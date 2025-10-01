from django.apps import apps

def current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return {'current_user': None, 'current_user_first_name': ''}
    try:
        Usuario = apps.get_model('usuarios', 'Usuario')
        user = Usuario.objects.filter(pk=user_id).first()
        if not user:
            return {'current_user': None, 'current_user_first_name': ''}
        first_name = user.nombre.split()[0] if getattr(user, 'nombre', None) else ''
        return {'current_user': user, 'current_user_first_name': first_name}
    except Exception:
        return {'current_user': None, 'current_user_first_name': ''}
