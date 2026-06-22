from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy

from apps.mascotas.models import Mascota
from apps.usuarios.models import Usuario
from .models import ConsultaMedica, HistoriaClinica
from .forms import FormularioConsulta, FormularioHistoriaClinica
from .services import puede_editar_consulta


# ─── Historia Clínica ────────────────────────────────────────────────────────

class ListaHistoriasClinicas(LoginRequiredMixin, ListView):
    model = HistoriaClinica
    template_name = 'historial/hc_lista.html'
    context_object_name = 'historias'
    paginate_by = 20

    def get_queryset(self):
        qs = HistoriaClinica.objects.select_related('mascota', 'mascota__dueno', 'creado_por')
        if self.request.user.es_dueno():
            qs = qs.filter(mascota__dueno=self.request.user)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(numero_hc__icontains=q) |
                Q(mascota__nombre__icontains=q) |
                Q(propietario_nombre__icontains=q) |
                Q(diagnostico_definitivo__icontains=q)
            )
        estado = self.request.GET.get('estado', '')
        if estado in (HistoriaClinica.ESTADO_ACTIVA, HistoriaClinica.ESTADO_CERRADA):
            qs = qs.filter(estado=estado)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['estado_filtro'] = self.request.GET.get('estado', '')
        return ctx


class CrearHistoriaClinica(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = HistoriaClinica
    form_class = FormularioHistoriaClinica
    template_name = 'historial/hc_form.html'

    def test_func(self) -> bool:
        return self.request.user.es_admin() or self.request.user.es_veterinario()

    def get_initial(self):
        initial = super().get_initial()
        mascota_pk = self.kwargs.get('mascota_pk') or self.request.GET.get('mascota')
        if mascota_pk:
            try:
                mascota = Mascota.objects.select_related('dueno').get(pk=mascota_pk)
                initial['mascota'] = mascota
                dueno = mascota.dueno
                initial['propietario_nombre']    = dueno.get_full_name() or dueno.username
                initial['propietario_telefono']  = dueno.telefono
                initial['propietario_email']     = dueno.email
                initial['veterinario_responsable'] = self.request.user if self.request.user.es_veterinario() else None
            except Mascota.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        hc = form.save(commit=False)
        hc.creado_por = self.request.user
        hc.save()
        messages.success(self.request, f'Historia Clínica {hc.numero_hc} creada exitosamente.')
        return redirect(reverse('hc_detalle', kwargs={'pk': hc.pk}))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nueva Historia Clínica'
        ctx['veterinarios'] = Usuario.objects.filter(rol=Usuario.ROL_VETERINARIO)
        return ctx


class DetalleHistoriaClinica(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = HistoriaClinica
    template_name = 'historial/hc_detalle.html'
    context_object_name = 'hc'

    def test_func(self) -> bool:
        hc = self.get_object()
        if self.request.user.es_dueno():
            return hc.mascota.dueno == self.request.user
        return True


class EditarHistoriaClinica(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = HistoriaClinica
    form_class = FormularioHistoriaClinica
    template_name = 'historial/hc_form.html'

    def test_func(self) -> bool:
        return self.request.user.es_admin() or self.request.user.es_veterinario()

    def form_valid(self, form):
        hc = form.save()
        messages.success(self.request, f'Historia Clínica {hc.numero_hc} actualizada.')
        return redirect(reverse('hc_detalle', kwargs={'pk': hc.pk}))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar {self.object.numero_hc}'
        ctx['veterinarios'] = Usuario.objects.filter(rol=Usuario.ROL_VETERINARIO)
        return ctx


class EliminarHistoriaClinica(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = HistoriaClinica
    template_name = 'historial/hc_confirmar_eliminar.html'
    success_url = reverse_lazy('hc_lista')

    def test_func(self) -> bool:
        return self.request.user.es_admin()

    def form_valid(self, form):
        messages.success(self.request, 'Historia Clínica eliminada.')
        return super().form_valid(form)


class DescargarPDFHistoriaClinica(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self) -> bool:
        hc = get_object_or_404(HistoriaClinica, pk=self.kwargs['pk'])
        if self.request.user.es_dueno():
            return hc.mascota.dueno == self.request.user
        return True

    def get(self, request, pk):
        hc = get_object_or_404(HistoriaClinica, pk=pk)
        try:
            from xhtml2pdf import pisa
        except ImportError:
            messages.error(request, 'La generación de PDF no está disponible. Instalá xhtml2pdf.')
            return redirect(reverse('hc_detalle', kwargs={'pk': pk}))

        template = get_template('historial/hc_pdf.html')
        html = template.render({'hc': hc}, request)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="HC-{hc.numero_hc}.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF.', status=500)
        return response


class HistorialMascota(LoginRequiredMixin, ListView):
    template_name = 'historial/lista.html'
    context_object_name = 'consultas'

    def get_mascota(self):
        mascota_pk = self.kwargs['mascota_pk']
        usuario = self.request.user
        if usuario.es_dueno():
            return get_object_or_404(Mascota, pk=mascota_pk, dueno=usuario)
        return get_object_or_404(Mascota, pk=mascota_pk)

    def get_queryset(self):
        return ConsultaMedica.objects.filter(
            mascota=self.get_mascota()
        ).select_related('veterinario')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mascota'] = self.get_mascota()
        ctx['consultas_editables'] = {
            c.pk for c in ctx['consultas'] if puede_editar_consulta(c)
        }
        return ctx


class CrearConsulta(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ConsultaMedica
    form_class = FormularioConsulta
    template_name = 'historial/formulario.html'

    def test_func(self):
        return self.request.user.es_veterinario() or self.request.user.es_admin()

    def get_mascota(self):
        return get_object_or_404(Mascota, pk=self.kwargs['mascota_pk'])

    def form_valid(self, form):
        consulta = form.save(commit=False)
        consulta.mascota = self.get_mascota()
        consulta.veterinario = self.request.user
        consulta.save()
        messages.success(self.request, 'Consulta médica registrada exitosamente.')
        return redirect(reverse('historial_mascota', kwargs={'mascota_pk': consulta.mascota.pk}))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mascota'] = self.get_mascota()
        ctx['titulo'] = 'Nueva Consulta Médica'
        return ctx


class EditarConsulta(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ConsultaMedica
    form_class = FormularioConsulta
    template_name = 'historial/formulario.html'

    def test_func(self):
        if not (self.request.user.es_veterinario() or self.request.user.es_admin()):
            return False
        consulta = self.get_object()
        return puede_editar_consulta(consulta)

    def form_valid(self, form):
        consulta = form.save()
        messages.success(self.request, 'Consulta médica actualizada.')
        return redirect(reverse('historial_mascota', kwargs={'mascota_pk': consulta.mascota.pk}))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mascota'] = self.object.mascota
        ctx['titulo'] = 'Editar Consulta Médica'
        return ctx
