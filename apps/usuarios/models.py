from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_ADMIN = 'admin'
    ROL_VETERINARIO = 'veterinario'
    ROL_RECEPCIONISTA = 'recepcionista'
    ROL_DUENO = 'dueno'

    ROLES = [
        (ROL_ADMIN, 'Administrador'),
        (ROL_VETERINARIO, 'Veterinario'),
        (ROL_RECEPCIONISTA, 'Recepcionista'),
        (ROL_DUENO, 'Dueño'),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default=ROL_DUENO, verbose_name='Rol')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def es_admin(self) -> bool:
        return self.rol == self.ROL_ADMIN

    def es_veterinario(self) -> bool:
        return self.rol == self.ROL_VETERINARIO

    def es_recepcionista(self) -> bool:
        return self.rol == self.ROL_RECEPCIONISTA

    def es_dueno(self) -> bool:
        return self.rol == self.ROL_DUENO

    def es_staff_clinica(self) -> bool:
        return self.rol in [self.ROL_ADMIN, self.ROL_VETERINARIO, self.ROL_RECEPCIONISTA]

    def puede_crear_dueno(self) -> bool:
        return self.rol in [self.ROL_ADMIN, self.ROL_VETERINARIO, self.ROL_RECEPCIONISTA]

    def get_rol_display_badge(self) -> str:
        colores = {
            self.ROL_ADMIN: 'bg-red-100 text-red-800',
            self.ROL_VETERINARIO: 'bg-blue-100 text-blue-800',
            self.ROL_RECEPCIONISTA: 'bg-yellow-100 text-yellow-800',
            self.ROL_DUENO: 'bg-green-100 text-green-800',
        }
        return colores.get(self.rol, 'bg-gray-100 text-gray-800')
