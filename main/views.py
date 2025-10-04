
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

def reservar(request):
	return render(request, 'main/reservar.html')
def admin(request):
	return render(request, 'main/adminpage.html')




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
                    telefono=telefono,
                    rol='CLIENTE',
                    password_hash=hashed
                )

            messages.success(request, "Registro exitoso. Por favor inicia sesión.")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Ya existe un usuario con ese correo o teléfono.")
            return render(request, 'main/registro.html')

    return render(request, 'main/registro.html')



def reservar(request):
    if request.method == 'POST':
        # Obtén los datos con request.POST.get('campo')
        # Guarda en la BD y redirige a una página de éxito
        ...
    return render(request, 'main/reservar.html')