from django.shortcuts import render
# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario

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


def login_view(request):
    """Vista de login: acepta email (o teléfono si quieres), valida y crea sesión."""
    if request.method == 'POST':
        # Leemos los campos del formulario (coinciden con la plantilla que te doy abajo)
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        # Puedes permitir login por teléfono si quieres:
        # If email contiene '@' -> buscar por email, else buscar por telefono
        user = None
        if email:
            try:
                if '@' in email:
                    user = Usuario.objects.get(email=email)
                else:
                    user = Usuario.objects.get(telefono=email)
            except Usuario.DoesNotExist:
                user = None

        if not user:
            messages.error(request, "Credenciales inválidas.")
            return render(request, 'main/login.html')

        if check_password(password, user.password_hash):
            # Guardamos datos mínimo en sesión
            request.session['user_id'] = user.id
            request.session['user_name'] = user.nombre
            # Opcional: tiempo de expiración (segundos). Por defecto usa SESSION_COOKIE_AGE
            # request.session.set_expiry(86400)
            messages.success(request, f"Bienvenido {user.nombre.split()[0]}!")
            return redirect('home')
        else:
            messages.error(request, "Credenciales inválidas.")
            return render(request, 'main/login.html')

    return render(request, 'main/login.html')


def logout_view(request):
    """Cerrar sesión mediante POST para seguridad."""
    if request.method == 'POST':
        request.session.flush()
        messages.info(request, "Has cerrado sesión.")
        return redirect('home')
    return redirect('home')

