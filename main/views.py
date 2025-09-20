
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password
from .models import Usuario

def home(request):
	return render(request, 'main/home.html')

def registro(request):
	return render(request, 'main/registro.html')

def habitaciones(request):
	return render(request, 'main/habitaciones.html')

def galeria(request):
	return render(request, 'main/galeria.html')

def login(request):
	return render(request, 'main/login.html')


def registro(request):
    if request.method == 'POST':
        nombre   = request.POST.get('firstName', '').strip()
        apellido = request.POST.get('lastName', '').strip()   # opcional: concatenar con nombre
        telefono = request.POST.get('phone', '').strip()
        email    = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password2= request.POST.get('password2', '')

        # Validaciones básicas
        if not (nombre and email and password and password2):
            messages.error(request, "Completa todos los campos obligatorios.")
            return render(request, 'registro.html')

        if password != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'registro.html')

        # Puedes aplicar validación adicional (regex teléfono, email)
        # Guardar en la tabla usuarios: concateno apellido al nombre si deseas
        nombre_completo = f"{nombre} {apellido}".strip()

        try:
            hashed = make_password(password)  # usa el hasher de Django (PBKDF2 por defecto)

            # Usar transacción para mayor seguridad
            with transaction.atomic():
                u = Usuario.objects.create(
                    nombre=nombre_completo,
                    email=email,
                    telefono=telefono,
                    rol='CLIENTE',            # por defecto
                    password_hash=hashed
                )

            messages.success(request, "Registro exitoso. Por favor inicia sesión.")
            return redirect('login')

        except IntegrityError as e:
            # Maneja duplicados (email único en la BD) o violaciones FK
            messages.error(request, "Ya existe un usuario con ese correo / teléfono.")
            return render(request, 'registro.html')

    # GET
    return render(request, 'main/registro.html')