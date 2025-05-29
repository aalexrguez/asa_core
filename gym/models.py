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

"""ENTRENADORES"""
class EntrenadorInfo(models.Model):
    entrenador = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100)
    dias_disponibles = models.CharField(max_length=100)  # Ej: "Lunes,Miércoles,Viernes"
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.entrenador.usuario_nombre} - {self.especialidad}"
    
class UsuarioEntrenador(models.Model):
    ue_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='cliente')
    ue_entrenador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='entrenador')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ue_cliente', 'ue_entrenador')

    def __str__(self):
        return f"{self.ue_cliente.username} asignado a {self.ue_entrenador.username}"
    
"""AVANCES FISICOS"""
class AvanceFisico(models.Model):
    cliente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'usuario_rol__ur_rolId': 1},
        related_name='avances_como_cliente'  # ← ¡aquí!
    )
    entrenador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'usuario_rol__ur_rolId': 2},
        related_name='avances_asignados'  # ← ¡y aquí!
    )
    fecha = models.DateField()
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    estatura = models.PositiveIntegerField(help_text="En centímetros")
    grasa_corporal = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cliente.username} - {self.fecha}"

    class Meta:
        ordering = ['-fecha']


