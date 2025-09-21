

from usuarios.models import Usuario

# usuarios/context_processors.py
from django.apps import apps

def current_user(request):
    """
    Context processor seguro que evita importaciones a nivel módulo
    (previene import cycles / recursion during Django startup).
    Devuelve current_user (objeto Usuario) y current_user_first_name.
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return {'current_user': None, 'current_user_first_name': ''}

    try:
        # Importar el modelo de forma dinámica para evitar import circular durante startup
        Usuario = apps.get_model('usuarios', 'Usuario')  # app_label, ModelName
        user = Usuario.objects.filter(pk=user_id).first()
        if not user:
            return {'current_user': None, 'current_user_first_name': ''}

        first_name = (user.nombre.split()[0] if getattr(user, 'nombre', None) else '')
        return {'current_user': user, 'current_user_first_name': first_name}
    except Exception:
        # En caso de cualquier fallo, no romper renderizado. Mejor devolver None.
        return {'current_user': None, 'current_user_first_name': ''}
