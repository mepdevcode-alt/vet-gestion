import io
import qrcode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

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
        usuario = self.request.user
        if usuario.es_admin() or usuario.es_veterinario():
            return True
        if usuario.es_dueno():
            return Mascota.objects.filter(pk=self.kwargs['pk'], dueno=usuario).exists()
        return False

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


class InfoCollarPublica(View):
    """Página pública accesible desde el QR del collar — sin login requerido."""

    def get(self, request, token):
        mascota = get_object_or_404(Mascota, token_collar=token)
        return render(request, 'mascotas/info_collar.html', {'mascota': mascota})


class QRCollarMascota(LoginRequiredMixin, View):
    """Devuelve el QR del collar como imagen PNG."""

    def _tiene_acceso(self, usuario, mascota: Mascota) -> bool:
        if usuario.es_dueno():
            return mascota.dueno == usuario
        return usuario.es_staff_clinica()

    def get(self, request, pk):
        if request.user.es_dueno():
            mascota = get_object_or_404(Mascota, pk=pk, dueno=request.user)
        else:
            mascota = get_object_or_404(Mascota, pk=pk)

        if not self._tiene_acceso(request.user, mascota):
            return HttpResponse(status=403)

        url_publica = request.build_absolute_uri(
            reverse('info_collar', kwargs={'token': mascota.token_collar})
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url_publica)
        qr.make(fit=True)
        imagen = qr.make_image(fill_color='black', back_color='white')

        buffer = io.BytesIO()
        imagen.save(buffer, format='PNG')
        buffer.seek(0)

        descargar = request.GET.get('descargar')
        response = HttpResponse(buffer.getvalue(), content_type='image/png')
        if descargar:
            nombre = f'qr-collar-{mascota.nombre.lower().replace(" ", "-")}.png'
            response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
