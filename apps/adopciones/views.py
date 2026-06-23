from django.views.generic import ListView, DetailView
from .models import MascotaAdopcion


class ListaAdopciones(ListView):
    model = MascotaAdopcion
    template_name = 'adopciones/lista.html'
    context_object_name = 'mascotas'
    paginate_by = 9

    def get_queryset(self):
        qs = MascotaAdopcion.objects.filter(disponible=True)
        busqueda = self.request.GET.get('q', '').strip()
        especie = self.request.GET.get('especie', '').strip()
        raza = self.request.GET.get('raza', '').strip()
        if busqueda:
            qs = qs.filter(nombre__icontains=busqueda)
        if especie:
            qs = qs.filter(especie=especie)
        if raza:
            qs = qs.filter(raza__icontains=raza)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['busqueda'] = self.request.GET.get('q', '')
        ctx['especie_activa'] = self.request.GET.get('especie', '')
        ctx['raza_activa'] = self.request.GET.get('raza', '')
        ctx['especies'] = MascotaAdopcion.ESPECIES
        todas = MascotaAdopcion.objects.all()
        ctx['stats'] = {
            'total': todas.count(),
            'perros': todas.filter(especie='perro').count(),
            'gatos': todas.filter(especie='gato').count(),
            'disponibles': todas.filter(disponible=True).count(),
        }
        return ctx


class DetalleAdopcion(DetailView):
    model = MascotaAdopcion
    template_name = 'adopciones/detalle.html'
    context_object_name = 'mascota'

    def get_queryset(self):
        return MascotaAdopcion.objects.filter(disponible=True)


class MisFavoritos(ListView):
    model = MascotaAdopcion
    template_name = 'adopciones/favoritos.html'
    context_object_name = 'mascotas'

    def get_queryset(self):
        return MascotaAdopcion.objects.filter(disponible=True)
