from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
"""USUARIOS"""
class Usuario(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    usuario_nombre = models.CharField(max_length=50)
    usuario_apellidos = models.CharField(max_length=120)
    usuario_email = models.EmailField()
    usuario_password = models.CharField(max_length=255)
    usuario_status = models.BooleanField(default=True)
    usuario_fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_imagen = models.ImageField(upload_to='usuarios',null=True,blank=True)

    def __str__(self):
        return self.username
    

class Rol(models.Model):
    rol_id = models.AutoField(primary_key=True)
    rol_nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.rol_nombre

class Usuario_rol(models.Model):
    ur_id = models.AutoField(primary_key=True)
    ur_username = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    ur_rolId = models.ForeignKey(Rol,on_delete=models.CASCADE)

"""MEMBRESIAS """

class TipoMembresia(models.Model):
    tm_id = models.AutoField(primary_key=True)
    tm_nombre = models.CharField(max_length=50)
    tm_precio = models.DecimalField(max_digits=8,decimal_places=2)
    tm_duracion_dias = models.PositiveIntegerField()

    def __str__(self):
        return self.tm_nombre

class Membresia(models.Model):
    mem_id = models.AutoField(primary_key=True)
    mem_tipo = models.ForeignKey(TipoMembresia,on_delete=models.PROTECT,null=True)
    mem_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE,null=True)
    mem_fecha_inicio = models.DateTimeField(auto_now_add=True,null=True)
    mem_fecha_fin = models.DateTimeField(blank=True, null=True)
    mem_status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.mem_fecha_inicio:
            self.mem_fecha_inicio = timezone.now()
        if not self.mem_fecha_fin and self.mem_tipo:
            self.mem_fecha_fin = self.mem_fecha_inicio + timedelta(days=self.mem_tipo.tm_duracion_dias)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.mem_tipo.tm_nombre if self.mem_tipo else "Sin tipo"
