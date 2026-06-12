from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.views import View
from django.urls import reverse_lazy

from .models import Turno
from .forms import FormularioSolicitarTurno, FormularioGestionarTurno


class ListaTurnos(LoginRequiredMixin, ListView):
    model = Turno
    template_name = 'turnos/lista.html'
    context_object_name = 'turnos'

    def get_queryset(self):
        usuario = self.request.user
        qs = Turno.objects.select_related('mascota', 'mascota__dueno', 'veterinario')
        if usuario.es_dueno():
            return qs.filter(mascota__dueno=usuario).order_by('-fecha_creacion')
        if usuario.es_veterinario():
            return qs.filter(veterinario=usuario).order_by('fecha_hora')
        return qs.order_by('-fecha_creacion')


class SolicitarTurno(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Turno
    form_class = FormularioSolicitarTurno
    template_name = 'turnos/formulario.html'
    success_url = reverse_lazy('lista_turnos')

    def test_func(self):
        return self.request.user.es_dueno()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Turno solicitado correctamente. Esperá la confirmación.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Solicitar Turno'
        return ctx


class DetalleTurno(LoginRequiredMixin, DetailView):
    model = Turno
    template_name = 'turnos/detalle.html'
    context_object_name = 'turno'

    def get_queryset(self):
        usuario = self.request.user
        if usuario.es_dueno():
            return Turno.objects.filter(mascota__dueno=usuario)
        return Turno.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form_gestion'] = FormularioGestionarTurno(instance=self.object)
        return ctx


class AprobarTurno(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def post(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk, estado=Turno.ESTADO_PENDIENTE)
        form = FormularioGestionarTurno(request.POST, instance=turno)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.estado = Turno.ESTADO_APROBADO
            turno.save()
            messages.success(request, f'Turno de {turno.mascota.nombre} aprobado.')
        else:
            messages.error(request, 'No se pudo aprobar el turno.')
        return redirect('lista_turnos')


class RechazarTurno(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def post(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk, estado=Turno.ESTADO_PENDIENTE)
        turno.notas_recepcion = request.POST.get('notas_recepcion', '')
        turno.estado = Turno.ESTADO_RECHAZADO
        turno.save()
        messages.warning(request, f'Turno de {turno.mascota.nombre} rechazado.')
        return redirect('lista_turnos')


class CompletarTurno(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.es_veterinario() or self.request.user.es_admin()

    def post(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk, estado=Turno.ESTADO_APROBADO)
        turno.estado = Turno.ESTADO_COMPLETADO
        turno.save()
        messages.success(request, f'Turno de {turno.mascota.nombre} marcado como completado.')
        return redirect('lista_turnos')
