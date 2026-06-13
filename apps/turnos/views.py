from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.views import View
from django.urls import reverse_lazy, reverse

from .models import Turno
from .forms import FormularioSolicitarTurno, FormularioRechazarTurno, FormularioCancelarTurno
from . import services


class MisTurnosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Turno
    template_name = 'turnos/mis_turnos.html'
    context_object_name = 'turnos'

    def test_func(self):
        return self.request.user.es_dueno()

    def get_queryset(self):
        return Turno.objects.filter(
            mascota__dueno=self.request.user
        ).select_related('mascota', 'veterinario').order_by('-fecha_creacion')


class SolicitarTurnoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Turno
    form_class = FormularioSolicitarTurno
    template_name = 'turnos/solicitar.html'
    success_url = reverse_lazy('turnos:mis_turnos')

    def test_func(self):
        return self.request.user.es_dueno()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.mascotas.models import Mascota
        ctx['tiene_mascotas'] = Mascota.objects.filter(dueno=self.request.user).exists()
        ctx['duraciones'] = Turno.DURACIONES_POR_TIPO
        return ctx

    def form_valid(self, form):
        datos = {
            'mascota':       form.cleaned_data['mascota'],
            'veterinario':   form.cleaned_data.get('veterinario'),
            'tipo_consulta': form.cleaned_data['tipo_consulta'],
            'fecha_hora':    form.cleaned_data['fecha_hora'],
            'motivo':        form.cleaned_data['motivo'],
        }
        try:
            services.crear_turno(self.request.user, datos)
            messages.success(self.request, 'Turno solicitado correctamente. Esperá la confirmación.')
            return redirect(self.success_url)
        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)


class GestionTurnosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Turno
    template_name = 'turnos/gestion.html'
    context_object_name = 'turnos'

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def get_queryset(self):
        qs = Turno.objects.select_related('mascota', 'mascota__dueno', 'veterinario')
        estado = self.request.GET.get('estado', Turno.ESTADO_PENDIENTE)
        if estado:
            qs = qs.filter(estado=estado)
        veterinario_id = self.request.GET.get('veterinario')
        if veterinario_id:
            qs = qs.filter(veterinario_id=veterinario_id)
        fecha = self.request.GET.get('fecha')
        if fecha:
            qs = qs.filter(fecha_hora__date=fecha)
        return qs.order_by('fecha_hora')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from apps.usuarios.models import Usuario
        ctx['estados'] = Turno.ESTADOS
        ctx['veterinarios'] = Usuario.objects.filter(rol=Usuario.ROL_VETERINARIO)
        ctx['estado_activo'] = self.request.GET.get('estado', Turno.ESTADO_PENDIENTE)
        return ctx


class AprobarTurnoView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def post(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk)
        try:
            services.aprobar_turno(turno, request.user)
            messages.success(request, f'Turno de {turno.mascota.nombre} aprobado correctamente.')
        except ValidationError as e:
            messages.error(request, e.message)
        return redirect(reverse('turnos:gestion'))


class RechazarTurnoView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = FormularioRechazarTurno
    template_name = 'turnos/rechazar.html'

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def get_turno(self):
        return get_object_or_404(Turno, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['turno'] = self.get_turno()
        return ctx

    def form_valid(self, form):
        turno = self.get_turno()
        motivo = form.cleaned_data['motivo_rechazo']
        try:
            services.rechazar_turno(turno, self.request.user, motivo)
            messages.warning(self.request, f'Turno de {turno.mascota.nombre} rechazado.')
        except ValidationError as e:
            messages.error(self.request, e.message)
        return redirect(reverse('turnos:gestion'))


class CancelarTurnoView(LoginRequiredMixin, FormView):
    form_class = FormularioCancelarTurno
    template_name = 'turnos/cancelar.html'

    def get_turno(self):
        turno = get_object_or_404(Turno, pk=self.kwargs['pk'])
        usuario = self.request.user
        if usuario.es_dueno() and turno.mascota.dueno != usuario:
            from django.http import Http404
            raise Http404
        return turno

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['turno'] = self.get_turno()
        return ctx

    def form_valid(self, form):
        turno = self.get_turno()
        motivo = form.cleaned_data['motivo_cancelacion']
        try:
            services.cancelar_turno(turno, self.request.user, motivo)
            messages.info(self.request, f'Turno de {turno.mascota.nombre} cancelado.')
        except ValidationError as e:
            messages.error(self.request, e.message)
            return self.form_invalid(form)

        if self.request.user.es_dueno():
            return redirect(reverse('turnos:mis_turnos'))
        return redirect(reverse('turnos:gestion'))


class CompletarTurnoView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def post(self, request, pk):
        turno = get_object_or_404(Turno, pk=pk)
        try:
            services.completar_turno(turno, request.user)
            messages.success(request, f'Turno de {turno.mascota.nombre} marcado como completado.')
        except ValidationError as e:
            messages.error(request, e.message)
        return redirect(reverse('turnos:gestion'))


class AgendaView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Turno
    template_name = 'turnos/agenda.html'
    context_object_name = 'turnos'

    def test_func(self):
        return self.request.user.es_admin() or self.request.user.es_recepcionista()

    def get_fecha(self):
        from datetime import date
        fecha_str = self.request.GET.get('fecha')
        if fecha_str:
            try:
                from datetime import datetime
                return datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                pass
        return date.today()

    def get_queryset(self):
        fecha = self.get_fecha()
        qs = Turno.objects.filter(
            estado=Turno.ESTADO_APROBADO,
            fecha_hora__date=fecha,
        ).select_related('mascota', 'mascota__dueno', 'veterinario').order_by('fecha_hora')

        veterinario_id = self.request.GET.get('veterinario')
        if veterinario_id:
            qs = qs.filter(veterinario_id=veterinario_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from datetime import timedelta
        from apps.usuarios.models import Usuario
        fecha = self.get_fecha()
        ctx['fecha'] = fecha
        ctx['fecha_anterior'] = (fecha - timedelta(days=1)).strftime('%Y-%m-%d')
        ctx['fecha_siguiente'] = (fecha + timedelta(days=1)).strftime('%Y-%m-%d')
        ctx['veterinarios'] = Usuario.objects.filter(rol=Usuario.ROL_VETERINARIO)
        ctx['veterinario_id'] = self.request.GET.get('veterinario', '')
        return ctx


class TurnosHoyVetView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Turno
    template_name = 'turnos/turnos_hoy_vet.html'
    context_object_name = 'turnos'

    def test_func(self):
        return self.request.user.es_veterinario()

    def get_queryset(self):
        hoy = timezone.localdate()
        return Turno.objects.filter(
            veterinario=self.request.user,
            estado=Turno.ESTADO_APROBADO,
            fecha_hora__date=hoy,
        ).select_related('mascota', 'mascota__dueno').order_by('fecha_hora')


class DetalleTurnoView(LoginRequiredMixin, DetailView):
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
        ctx['historial'] = self.object.historial_estados.select_related('realizado_por').order_by('fecha_hora')
        return ctx
