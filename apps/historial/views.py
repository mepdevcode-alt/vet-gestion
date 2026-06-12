from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse

from apps.mascotas.models import Mascota
from .models import ConsultaMedica
from .forms import FormularioConsulta
from .services import puede_editar_consulta


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
