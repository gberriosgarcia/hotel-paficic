from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password
from django.db import transaction

# Tu modelo real:
from main.models import Usuario  # tiene: id, email, nombre, password_hash, telefono, rol, creado_en

def _looks_like_django_hash(value: str) -> bool:
    if not value:
        return False
    # hashes Django típicos: pbkdf2_sha256$, argon2, bcrypt, scrypt
    prefixes = ('pbkdf2_', 'argon2', 'bcrypt', 'scrypt')
    return any(str(value).startswith(p) for p in prefixes)

class UsuarioEmailBackend(BaseBackend):
    """
    Autentica contra la tabla Usuario:
    - Identificador: email (case-insensitive)
    - Contraseña: password_hash (hash Django recomendado; si detecta texto plano, lo migra a hash)
    - Crea/sincroniza un auth_user espejo para sesiones y plantillas de Django.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = (username or '').strip().lower()
        if not email or not password:
            return None

        try:
            u = Usuario.objects.get(email__iexact=email)
        except Usuario.DoesNotExist:
            return None

        stored = (u.password_hash or '').strip()

        # 1) Verificar contraseña según el formato
        if _looks_like_django_hash(stored):
            # password_hash ya contiene un hash compatible con Django
            if not check_password(password, stored):
                return None
            new_hash = stored
        else:
            # Parece texto plano: compara directo y MIGRA a hash seguro
            if stored != password:
                return None
            new_hash = make_password(password)
            try:
                with transaction.atomic():
                    u.password_hash = new_hash
                    u.save(update_fields=['password_hash'])
            except Exception:
                # si por algún motivo no se pudo guardar, seguimos autenticando igual
                pass

        # 2) Sincronizar/crear auth_user espejo (username=email)
        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': u.nombre or ''}
        )

        updates = []
        if user.email != email:
            user.email = email
            updates.append('email')
        if (u.nombre or '') and user.first_name != u.nombre:
            user.first_name = u.nombre
            updates.append('first_name')
        if user.password != new_hash:
            user.password = new_hash
            updates.append('password')
        if not user.is_active:
            user.is_active = True
            updates.append('is_active')

        if updates:
            user.save(update_fields=updates)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

# Alias opcional si tu settings apunta a EmailBackend
EmailBackend = UsuarioEmailBackend


