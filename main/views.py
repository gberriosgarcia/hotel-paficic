# main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime
from decimal import Decimal

# Importa tus modelos reales
from .models import Usuario, Reserva, Habitacion

# ======================
# Configuración precios y adelanto
# ======================

# Si la habitación no trae precio desde BD, se usan estos valores por tipo
ROOM_PRICE = {'TURISTA': Decimal('90.00'), 'PREMIUM': Decimal('180.00')}
DEPOSIT_RATE = Decimal('0.30')  # 30%

def _normalizar_tipo(valor: str) -> str:
    v = (valor or '').strip().lower()
    if v in ('premium', 'premier', 'vip', 'suite'):
        return 'PREMIUM'
    return 'TURISTA'

def _calcular_adelanto_por_tipo(tipo: str) -> Decimal:
    base = ROOM_PRICE.get(_normalizar_tipo(tipo), ROOM_PRICE['TURISTA'])
    return (base * DEPOSIT_RATE).quantize(Decimal('0.01'))

def _calcular_adelanto_por_habitacion(habitacion) -> Decimal:
    """
    Si la habitación tiene precio en BD, usa 30% de ese precio.
    Si no, cae al mapa por tipo (TURISTA/PREMIUM).
    """
    try:
        if hasattr(habitacion, 'precio') and habitacion.precio is not None:
            return (Decimal(habitacion.precio) * DEPOSIT_RATE).quantize(Decimal('0.01'))
    except Exception:
        pass
    # Fallback por tipo si existe; si no, asume TURISTA
    tipo = getattr(habitacion, 'tipo', 'TURISTA')
    return _calcular_adelanto_por_tipo(tipo)

# ======================
# Vistas públicas básicas
# ======================

def home(request):
    return render(request, 'main/home.html')

def habitaciones(request):
    return render(request, 'main/habitaciones.html')

def galeria(request):
    return render(request, 'main/galeria.html')

def login(request):
    return render(request, 'main/login.html')

def admin(request):
    return render(request, 'main/adminpage.html')

# ======================
# Registro de usuarios
# ======================

def registro(request):
    if request.method == 'POST':
        nombre   = request.POST.get('firstName', '').strip()
        apellido = request.POST.get('lastName', '').strip()
        telefono = request.POST.get('phone', '').strip()
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password2= request.POST.get('password2', '')

        if not (nombre and email and password and password2):
            messages.error(request, "Completa todos los campos obligatorios.")
            return render(request, 'main/registro.html')

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'main/registro.html')

        nombre_completo = f"{nombre} {apellido}".strip()

        try:
            hashed = make_password(password)
            with transaction.atomic():
                Usuario.objects.create(
                    nombre=nombre_completo,
                    email=email,
                    telefono=telefono or None,
                    rol='CLIENTE',
                    password_hash=hashed
                )
            messages.success(request, "Registro exitoso. Por favor inicia sesión.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Ya existe un usuario con ese correo o teléfono.")
            return render(request, 'main/registro.html')

    return render(request, 'main/registro.html')

# ======================
# Reservas
# ======================

def reservar(request):
    """
    Inserta en la tabla 'reservas' usando las columnas reales:
    - cliente_id (desde Usuario por email del request.user)
    - habitacion_id (desde un <select> en el form con name="habitacion_id")
    - fecha_inicio (desde 'fecha_entrada')
    - fecha_fin    (desde 'fecha_salida')
    - estado       ('PENDIENTE')
    - monto_adelanto (30% del precio de la habitación o del tipo)
    """
    if request.method == 'POST':
        # Datos que SÍ se usan para grabar
        f1      = request.POST.get('fecha_entrada', '')
        f2      = request.POST.get('fecha_salida', '')
        tipo    = (request.POST.get('tipo', '') or '').strip()
        if (tipo =='turista'):
            hab_id  = 1
        else:
            hab_id  = 2     

        # Debug útil
        print("[DEBUG reservar]", timezone.now().isoformat(), {
            "fecha_entrada": f1, "fecha_salida": f2, "tipo": tipo, "habitacion_id": hab_id
        })

        # Validaciones básicas
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para reservar.")
            return redirect('login')

        if not (f1 and f2 and hab_id):
            messages.error(request, "Faltan datos obligatorios (fechas y habitación).")
            return redirect('reservar')

        try:
            fi = datetime.strptime(f1, '%Y-%m-%d').date()
            ff = datetime.strptime(f2, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Formato de fecha inválido (usa AAAA-MM-DD).")
            return redirect('reservar')

        if fi > ff:
            messages.error(request, "La fecha de llegada no puede ser posterior a la de salida.")
            return redirect('reservar')

        # Buscar cliente en tu tabla 'usuarios' por el email del usuario autenticado
        cliente = Usuario.objects.filter(email=request.user.email).first()
        if not cliente:
            messages.error(request, "Tu cuenta no está vinculada al registro de clientes.")
            return redirect('reservar')

        # Verificar habitación
        habitacion = Habitacion.objects.filter(id=hab_id).first()
        if not habitacion:
            messages.error(request, "La habitación seleccionada no existe.")
            return redirect('reservar')

        # Calcular adelanto (30%). Si la habitación tiene precio, úsalo; si no, usa 'tipo'
        adelanto = _calcular_adelanto_por_habitacion(habitacion)
        # Si además quieres respetar el selector de tipo del formulario (por ejemplo, si la misma
        # habitación puede tarificarse distinto), descomenta la línea siguiente:
        # adelanto = _calcular_adelanto_por_tipo(tipo)

        # Insertar en la tabla 'reservas' (columnas reales)
        with transaction.atomic():
            Reserva.objects.create(
                cliente=cliente,              # FK -> cliente_id
                habitacion=habitacion,        # FK -> habitacion_id
                fecha_inicio=fi,
                fecha_fin=ff,
                estado='PENDIENTE',
                monto_adelanto=adelanto,
            )

        messages.success(request, f"Reserva registrada. Adelanto (30%): USD {adelanto}.")
        return redirect('home')

    # GET: pasar habitaciones para el <select name="habitacion_id">
    habitaciones = Habitacion.objects.all().order_by('id')
    return render(request, 'main/reservar.html', {'habitaciones': habitaciones})

