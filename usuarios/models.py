from django.db import models

# Create your models here.
# usuarios/models.py
from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    email = models.CharField(max_length=150, unique=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rol = models.CharField(max_length=10)  # ejemplo: 'CLIENTE','EMPLEADO','ADMIN'
    password_hash = models.CharField(max_length=255)
    creado_en = models.DateTimeField()

    class Meta:
        db_table = 'usuarios'
        managed = False   # la tabla ya existe en MySQL; Django no la creará

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
