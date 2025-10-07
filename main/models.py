# main/models.py
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


# === (Opcional) Modelo de habitaciones si tu DB tiene la tabla 'habitaciones' ===
# Si aún no la tienes, puedes omitir esta clase y usar IntegerField en Reserva (habitacion_id).
class Habitacion(models.Model):
    id = models.AutoField(primary_key=True)
    # Ajusta estos campos a tu esquema real de 'habitaciones'
    tipo = models.CharField(max_length=20, blank=True, null=True)  # 'TURISTA' / 'PREMIUM', etc.
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'habitaciones'
        managed = False

    def __str__(self):
        return f"Habitación {self.id} ({self.tipo or 's/tipo'})"


# === Modelo de reservas (alineado con tu tabla existente) ===
class Reserva(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'PENDIENTE'),
        ('CONFIRMADA', 'CONFIRMADA'),
        ('CANCELADA', 'CANCELADA'),
        ('CHECKIN', 'CHECKIN'),
        ('CHECKOUT', 'CHECKOUT'),
    )

    id = models.AutoField(primary_key=True)

    # FK a usuarios.cliente_id (columna real en la DB)
    cliente = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column='cliente_id',
        related_name='reservas'
    )

    # FK a habitaciones.habitacion_id (columna real en la DB).
    # Si no tienes la tabla 'habitaciones', reemplaza por:
    # habitacion_id = models.IntegerField()
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        db_column='habitacion_id',
        related_name='reservas'
    )

    # Fechas con nombres EXACTOS de la DB
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    # Enum en MySQL; aquí lo mapeamos a CharField con choices
    estado = models.CharField(max_length=12, choices=ESTADOS, default='PENDIENTE')

    monto_adelanto = models.DecimalField(max_digits=10, decimal_places=2)

    # Timestamp en la DB
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creado_en')

    class Meta:
        db_table = 'reservas'   # nombre EXACTO de la tabla MySQL
        managed = False         # ¡Clave! No toques esta tabla con migrations

    def __str__(self):
        return f"Reserva #{self.id} · Cliente {self.cliente_id} · Hab {getattr(self, 'habitacion_id', None)} · {self.fecha_inicio} → {self.fecha_fin}"

    # --- Helpers opcionales para acceder a datos del cliente ---
    @property
    def nombre_cliente(self):
        return getattr(self.cliente, 'nombre', None)

    @property
    def email_cliente(self):
        return getattr(self.cliente, 'email', None)
