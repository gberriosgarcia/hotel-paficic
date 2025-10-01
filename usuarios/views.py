# usuarios/views.py (reemplaza login_view por esto - DEBUG temporal)
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario
from django.contrib.auth.views import LoginView

def login_view(request):
    debug = {'step': None, 'identifier': None, 'found_user': False, 'check_password': None, 'session_before': None}
    debug['session_before'] = dict(request.session)

    if request.method == 'POST':
        identifier = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''
        debug['step'] = 'POST received'
        debug['identifier'] = identifier

        if not identifier or not password:
            debug['step'] = 'missing fields'
            messages.error(request, "Completa email y contraseña.")
            return render(request, 'main/login.html', {'debug': debug})

        # buscar por email o telefono
        user = None
        try:
            if '@' in identifier:
                user = Usuario.objects.get(email=identifier.lower())
            else:
                user = Usuario.objects.get(telefono=identifier)
            debug['found_user'] = True
            debug['user_id'] = user.id
        except Usuario.DoesNotExist:
            debug['step'] = 'user not found'
            messages.error(request, "Credenciales inválidas.")
            return render(request, 'main/login.html', {'debug': debug})

        # verificar contraseña
        try:
            ok = check_password(password, user.password_hash)
            debug['check_password'] = ok
        except Exception as e:
            debug['check_password'] = f'error: {e}'
            ok = False

        if ok:
            request.session['user_id'] = user.id
            request.session['user_name'] = user.nombre
            debug['session_after'] = dict(request.session)
            messages.success(request, f"Bienvenido {user.nombre.split()[0]}!")
            print("DEBUG LOGIN OK:", debug)
            return redirect('home')
        else:
            debug['step'] = 'invalid password'
            messages.error(request, "Credenciales inválidas.")
            print("DEBUG LOGIN FAIL:", debug)
            return render(request, 'main/login.html', {'debug': debug})

    # GET
    return render(request, 'main/login.html')


class EmailLoginView(LoginView):
    template_name = 'usuarios/login.html'

    def form_valid(self, form):
        # login ya ejecutado por super
        remember = self.request.POST.get('rememberMe')
        # si el usuario NO marcó 'remember', expirar al cerrar navegador
        if not remember:
            self.request.session.set_expiry(0)
        else:
            # Duración en segundos (ejemplo: 2 semanas)
            self.request.session.set_expiry(1209600)
        return super().form_valid(form)