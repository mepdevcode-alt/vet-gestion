from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Mascota
from .forms import FormularioMascota


class ListaMascotas(LoginRequiredMixin, ListView):
    model = Mascota
    template_name = 'mascotas/lista.html'
    context_object_name = 'mascotas'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.es_dueno():
            return Mascota.objects.filter(dueno=usuario).select_related('dueno')
        return Mascota.objects.all().select_related('dueno')


class DetalleMascota(LoginRequiredMixin, DetailView):
    model = Mascota
    template_name = 'mascotas/detalle.html'
    context_object_name = 'mascota'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.es_dueno():
            return Mascota.objects.filter(dueno=usuario)
        return Mascota.objects.all()


class CrearMascota(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Mascota
    form_class = FormularioMascota
    template_name = 'mascotas/formulario.html'
    success_url = reverse_lazy('lista_mascotas')

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_veterinario()

    def form_valid(self, form):
        messages.success(self.request, f'Mascota "{form.instance.nombre}" creada exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nueva Mascota'
        ctx['accion'] = 'Crear'
        return ctx


class EditarMascota(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mascota
    form_class = FormularioMascota
    template_name = 'mascotas/formulario.html'
    success_url = reverse_lazy('lista_mascotas')

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_veterinario()

    def form_valid(self, form):
        messages.success(self.request, f'Mascota "{form.instance.nombre}" actualizada.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar — {self.object.nombre}'
        ctx['accion'] = 'Guardar cambios'
        return ctx


class EliminarMascota(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mascota
    template_name = 'mascotas/confirmar_eliminar.html'
    success_url = reverse_lazy('lista_mascotas')
    context_object_name = 'mascota'

    def test_func(self):
        return self.request.user.es_admin()

    def form_valid(self, form):
        messages.success(self.request, f'Mascota eliminada.')
        return super().form_valid(form)
