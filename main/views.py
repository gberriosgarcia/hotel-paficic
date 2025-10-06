# main/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from .models import Usuario, Reserva

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

ROOM_PRICE = {'TURISTA': Decimal('90.00'), 'PREMIUM': Decimal('180.00')}
DEPOSIT_RATE = Decimal('0.30')  # 30% obligatorio

def _normalizar_tipo(valor: str) -> str:
    v = (valor or '').strip().lower()
    if v in ('premium', 'premier', 'vip', 'suite'):
        return 'PREMIUM'
    return 'TURISTA'

def _calcular_adelanto(tipo: str):
    base = ROOM_PRICE.get(_normalizar_tipo(tipo), ROOM_PRICE['TURISTA'])
    adelanto = (base * DEPOSIT_RATE).quantize(Decimal('0.01'))
    return base, adelanto

def reservar(request):
    if request.method == 'POST':
        nombre  = request.POST.get('nombre','').strip()
        email   = request.POST.get('email','').strip().lower()
        tel     = request.POST.get('telefono','').strip()
        f1      = request.POST.get('fecha_entrada','')
        f2      = request.POST.get('fecha_salida','')
        tipo    = request.POST.get('tipo','').strip()

        # FIX: usar timezone.now()
        print("[DEBUG reservar]", timezone.now().isoformat(), {
            "nombre": bool(nombre), "email": bool(email), "telefono": bool(tel),
            "fecha_entrada": f1, "fecha_salida": f2, "tipo": tipo
        })

        if not (nombre and email and f1 and f2 and tipo):
            messages.error(request, "Faltan datos obligatorios.")
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

        # Precio y adelanto (30%)
        _, adelanto = _calcular_adelanto(tipo)

        # Guardar en tu tabla 'reservas'
        Reserva.objects.create(
            nombre=nombre,
            email=email,
            telefono=tel or None,
            fecha_entrada=fi,
            fecha_salida=ff,
            tipo=_normalizar_tipo(tipo),
            estado='PENDIENTE',
            monto_adelanto=adelanto,
        )

        messages.success(request, f"Reserva registrada. Adelanto (30%): USD {adelanto}.")
        return redirect('home')

    return render(request, 'main/reservar.html')
