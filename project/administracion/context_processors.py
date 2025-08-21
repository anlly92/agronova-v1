from .models import Administrador

def admin_es_principal(request):
    if request.user.is_authenticated:
        try:
            admin = Administrador.objects.get(correo=request.user.username)
            return {'admin_es_principal': admin.es_principal}
        except Administrador.DoesNotExist:
            pass
    return {'admin_es_principal': False}

# esto lo permite usar directamente en las plantillas html