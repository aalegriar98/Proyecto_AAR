from django.contrib import admin
from .models import Rol, Usuario, Categoria, Herramienta, Prestamo, Mantenimiento

admin.site.register(Rol)
admin.site.register(Usuario)
admin.site.register(Categoria)
admin.site.register(Herramienta)
admin.site.register(Prestamo)
admin.site.register(Mantenimiento)