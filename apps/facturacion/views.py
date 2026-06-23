import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, TemplateView

from apps.turnos.models import Turno
from .forms import FormularioCambiarEstado, FormularioFactura, ItemFormSet
from .models import Factura, ItemFactura, PagoMercadoPago

logger = logging.getLogger(__name__)


class ListaFacturas(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'facturacion/lista.html'
    context_object_name = 'facturas'

    def get_queryset(self):
        usuario = self.request.user
        qs = Factura.objects.select_related('dueno', 'turno', 'turno__mascota')
        if usuario.es_dueno():
            return qs.filter(dueno=usuario)
        return qs.all()


class DetalleFactura(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = 'facturacion/detalle.html'
    context_object_name = 'factura'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.es_dueno():
            return Factura.objects.filter(dueno=usuario)
        return Factura.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['items'] = self.object.items.all()
        ctx['form_estado'] = FormularioCambiarEstado(instance=self.object)
        return ctx


class CrearFactura(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'facturacion/formulario.html'

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def get_turno(self):
        return get_object_or_404(Turno, pk=self.kwargs['turno_pk'], estado=Turno.ESTADO_COMPLETADO)

    def get(self, request, turno_pk):
        turno = self.get_turno()
        factura_existente = Factura.objects.filter(turno=turno).first()
        if factura_existente:
            messages.warning(request, 'Este turno ya tiene una factura.')
            return redirect(reverse('detalle_factura', kwargs={'pk': factura_existente.pk}))
        form = FormularioFactura()
        formset = ItemFormSet()
        return self._render(request, form, formset, turno)

    def post(self, request, turno_pk):
        turno = self.get_turno()
        form = FormularioFactura(request.POST)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                factura = form.save(commit=False)
                factura.turno = turno
                factura.dueno = turno.mascota.dueno
                factura.save()
                formset.instance = factura
                formset.save()
            messages.success(request, f'Factura #{factura.id} creada exitosamente.')
            return redirect(reverse('detalle_factura', kwargs={'pk': factura.pk}))
        return self._render(request, form, formset, turno)

    def _render(self, request, form, formset, turno):
        from django.shortcuts import render
        return render(request, self.template_name, {
            'form': form,
            'formset': formset,
            'turno': turno,
        })


class CambiarEstadoFactura(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def post(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        form = FormularioCambiarEstado(request.POST, instance=factura)
        if form.is_valid():
            form.save()
            messages.success(request, f'Estado de factura #{factura.id} actualizado.')
        else:
            messages.error(request, 'Estado inválido.')
        return redirect(reverse('detalle_factura', kwargs={'pk': pk}))


class IniciarPagoMP(LoginRequiredMixin, View):
    """Crea la preferencia en Mercado Pago y redirige al checkout."""

    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)

        if factura.dueno != request.user:
            messages.error(request, 'No tenés permiso para pagar esta factura.')
            return redirect(reverse('detalle_factura', kwargs={'pk': pk}))

        if factura.estado != Factura.ESTADO_PENDIENTE:
            messages.warning(request, 'Esta factura no está pendiente de pago.')
            return redirect(reverse('detalle_factura', kwargs={'pk': pk}))

        import mercadopago
        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

        items = [
            {
                'title': item.descripcion,
                'quantity': item.cantidad,
                'unit_price': float(item.precio_unitario),
                'currency_id': 'ARS',
            }
            for item in factura.items.all()
        ]

        base_url = settings.MP_WEBHOOK_URL.replace('/facturacion/webhook/mp/', '') if settings.MP_WEBHOOK_URL else None

        def back_url(name):
            path = reverse(name, kwargs={'pk': pk})
            return f'{base_url}{path}' if base_url else request.build_absolute_uri(path)

        preference_data = {
            'items': items,
            'payer': {
                'name': factura.dueno.first_name or factura.dueno.username,
                'surname': factura.dueno.last_name,
                'email': factura.dueno.email,
            },
            'back_urls': {
                'success': back_url('pago_exitoso_mp'),
                'pending': back_url('pago_pendiente_mp'),
                'failure': back_url('pago_fallido_mp'),
            },
            'external_reference': str(factura.pk),
        }

        if base_url:
            preference_data['auto_return'] = 'approved'
            preference_data['notification_url'] = settings.MP_WEBHOOK_URL

        result = sdk.preference().create(preference_data)
        preference = result.get('response', {})

        if result.get('status') not in (200, 201):
            logger.error('Error al crear preferencia MP: %s', result)
            messages.error(request, 'No se pudo iniciar el pago. Intentá de nuevo.')
            return redirect(reverse('detalle_factura', kwargs={'pk': pk}))

        PagoMercadoPago.objects.create(
            factura=factura,
            preference_id=preference['id'],
        )

        # En sandbox usar sandbox_init_point; en producción usar init_point
        redirect_url = preference.get('sandbox_init_point') or preference.get('init_point')
        return redirect(redirect_url)


@method_decorator(csrf_exempt, name='dispatch')
class WebhookMP(View):
    """Recibe notificaciones de pago de Mercado Pago."""

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # MP envía notificaciones tipo "payment"
        if data.get('type') != 'payment':
            return HttpResponse(status=200)

        payment_id = str(data.get('data', {}).get('id', ''))
        if not payment_id:
            return HttpResponse(status=400)

        import mercadopago
        sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
        result = sdk.payment().get(payment_id)

        if result.get('status') != 200:
            logger.error('No se pudo obtener el pago %s de MP', payment_id)
            return HttpResponse(status=200)

        payment_info = result['response']
        estado_mp = payment_info.get('status', '')
        factura_id = payment_info.get('external_reference', '')

        if not factura_id:
            return HttpResponse(status=200)

        try:
            factura = Factura.objects.get(pk=factura_id)
        except Factura.DoesNotExist:
            logger.warning('Webhook MP: factura %s no encontrada', factura_id)
            return HttpResponse(status=200)

        # Actualizar el registro de pago o crearlo si no existe (idempotente)
        pago, _ = PagoMercadoPago.objects.get_or_create(
            payment_id=payment_id,
            defaults={
                'factura': factura,
                'preference_id': payment_info.get('preference_id', ''),
                'estado_mp': estado_mp,
            },
        )
        if pago.estado_mp != estado_mp:
            pago.estado_mp = estado_mp
            pago.save(update_fields=['estado_mp', 'fecha_actualizacion'])

        if estado_mp == PagoMercadoPago.ESTADO_APROBADO and factura.estado == Factura.ESTADO_PENDIENTE:
            with transaction.atomic():
                Factura.objects.filter(pk=factura.pk, estado=Factura.ESTADO_PENDIENTE).update(
                    estado=Factura.ESTADO_PAGADO
                )
            logger.info('Factura #%s marcada como pagada via MP (payment_id=%s)', factura.pk, payment_id)

        return HttpResponse(status=200)


class PagoExitosoMP(LoginRequiredMixin, View):
    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk, dueno=request.user)
        return render(request, 'facturacion/pago_exitoso.html', {'factura': factura})


class PagoPendienteMP(LoginRequiredMixin, View):
    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk, dueno=request.user)
        return render(request, 'facturacion/pago_pendiente.html', {'factura': factura})


class PagoFallidoMP(LoginRequiredMixin, View):
    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk, dueno=request.user)
        return render(request, 'facturacion/pago_fallido.html', {'factura': factura})
