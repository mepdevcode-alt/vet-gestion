from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
from django.urls import reverse_lazy, reverse
from django.db import transaction

from apps.turnos.models import Turno
from .models import Factura, ItemFactura
from .forms import FormularioFactura, ItemFormSet, FormularioCambiarEstado


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
