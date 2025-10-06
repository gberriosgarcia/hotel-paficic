from django.db import models


# === Modelo de usuarios (ya existente en tu base de datos) ===
class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    email = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    rol = models.CharField(max_length=10)  # 'CLIENTE', 'EMPLEADO', 'ADMIN'
    password_hash = models.CharField(max_length=255)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'     # nombre EXACTO de la tabla MySQL
        managed = False           # Django no aplicará migrations sobre esta tabla

    def __str__(self):
        return f"{self.nombre} ({self.email})"


# === Modelo de reservas ===
class Reserva(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'PENDIENTE'),
        ('CONFIRMADA', 'CONFIRMADA'),
        ('CANCELADA', 'CANCELADA'),
        ('CHECKIN', 'CHECKIN'),
        ('CHECKOUT', 'CHECKOUT'),
    )

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True, null=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    tipo = models.CharField(max_length=50)
    adultos = models.PositiveSmallIntegerField(default=1)
    ninos = models.PositiveSmallIntegerField(default=0)
    mensaje = models.TextField(blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default='PENDIENTE')
    monto_adelanto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reservas'     # nombre EXACTO de la tabla MySQL

    def __str__(self):
        return f"{self.nombre} ({self.fecha_entrada} → {self.fecha_salida})"
