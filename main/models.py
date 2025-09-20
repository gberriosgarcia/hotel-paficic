from django.db import models

from django.db import models

class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    email = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rol = models.CharField(max_length=10)  # 'CLIENTE','EMPLEADO','ADMIN'
    password_hash = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'     # nombre EXACTO de la tabla MySQL
        managed = False          # Django NO aplicará migrations sobre esta tabla

    def __str__(self):
        return f"{self.nombre} ({self.email})"