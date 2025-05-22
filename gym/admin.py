from django.contrib import admin
from .models import Usuario,Usuario_rol,Rol,Membresia,TipoMembresia
# Register your models here.

admin.site.register(Usuario)
admin.site.register(Usuario_rol)
admin.site.register(Rol)
admin.site.register(TipoMembresia)
admin.site.register(Membresia)