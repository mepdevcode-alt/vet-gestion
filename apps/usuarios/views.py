from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, TemplateView, ListView

from apps.mascotas.models import Mascota
from apps.turnos.models import Turno
from apps.facturacion.models import Factura
from .forms import FormularioLogin, FormularioCrearDueno
from .models import Usuario


class IniciarSesion(FormView):
    template_name = 'usuarios/login.html'
    form_class = FormularioLogin

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return redirect('dashboard')

    def form_invalid(self, form):
        messages.error(self.request, 'Usuario o contraseña incorrectos.')
        return super().form_invalid(form)


class CerrarSesion(View):
    def post(self, request):
        logout(request)
        return redirect('login')


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        usuario = request.user
        if usuario.es_admin():
            return redirect('dashboard_admin')
        elif usuario.es_veterinario():
            return redirect('dashboard_veterinario')
        elif usuario.es_recepcionista():
            return redirect('dashboard_recepcionista')
        else:
            return redirect('dashboard_dueno')


class DashboardAdmin(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'usuarios/dashboard_admin.html'

    def test_func(self):
        return self.request.user.es_admin()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.now().date()
        ctx['total_mascotas'] = Mascota.objects.count()
        ctx['turnos_pendientes'] = Turno.objects.filter(estado=Turno.ESTADO_PENDIENTE).count()
        ctx['consultas_hoy'] = 0
        ctx['facturas_pendientes'] = Factura.objects.filter(estado=Factura.ESTADO_PENDIENTE).count()
        ctx['turnos_recientes'] = Turno.objects.select_related('mascota', 'veterinario').order_by('-fecha_creacion')[:5]
        return ctx


class DashboardVeterinario(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'usuarios/dashboard_veterinario.html'

    def test_func(self):
        return self.request.user.es_veterinario()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        hoy = timezone.now().date()
        ctx['mis_turnos_hoy'] = Turno.objects.filter(
            veterinario=self.request.user,
            estado=Turno.ESTADO_APROBADO,
            fecha_hora__date=hoy,
        ).select_related('mascota')
        ctx['total_mis_turnos'] = Turno.objects.filter(
            veterinario=self.request.user,
            estado=Turno.ESTADO_APROBADO,
        ).count()
        return ctx


class DashboardRecepcionista(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'usuarios/dashboard_recepcionista.html'

    def test_func(self):
        return self.request.user.es_recepcionista()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['turnos_pendientes'] = Turno.objects.filter(
            estado=Turno.ESTADO_PENDIENTE,
        ).select_related('mascota', 'mascota__dueno').order_by('fecha_hora')[:10]
        ctx['facturas_pendientes'] = Factura.objects.filter(
            estado=Factura.ESTADO_PENDIENTE,
        ).select_related('dueno', 'turno')[:10]
        return ctx


class DashboardDueno(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'usuarios/dashboard_dueno.html'

    def test_func(self):
        return self.request.user.es_dueno()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['mis_mascotas'] = Mascota.objects.filter(dueno=self.request.user)
        ctx['mis_turnos'] = Turno.objects.filter(
            mascota__dueno=self.request.user,
        ).order_by('-fecha_creacion')[:5]
        ctx['mis_facturas'] = Factura.objects.filter(
            dueno=self.request.user,
        ).order_by('-fecha_emision')[:5]
        return ctx


class CrearDueno(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = 'usuarios/crear_dueno.html'
    form_class = FormularioCrearDueno

    def test_func(self):
        return self.request.user.puede_crear_dueno()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Cuenta de dueño creada exitosamente.')
        return redirect('lista_usuarios')

    def form_invalid(self, form):
        messages.error(self.request, 'Por favor corregí los errores del formulario.')
        return super().form_invalid(form)


class ListaUsuarios(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = 'usuarios/lista_usuarios.html'
    context_object_name = 'usuarios'
    ordering = ['rol', 'last_name', 'first_name']

    def test_func(self):
        return self.request.user.es_admin()
