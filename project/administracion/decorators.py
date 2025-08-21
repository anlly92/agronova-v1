from django.http import HttpResponseForbidden
# Se utiliza para devolver una respuesta HTTP 403 (Prohibido).
# Esto se muestra cuando el usuario intenta acceder a una vista que no tiene permiso para ver.

from django.contrib.auth.decorators import login_required
# Asegura que solo los usuarios autenticados (logueados) puedan acceder a la vista.
#Si el usuario no ha iniciado sesión, será redirigido automáticamente al login.

from administracion.models import Administrador
# Importa el modelo 'Administrador' que contiene información como si el usuario es principal o secundario.
# Necesitamos este modelo para verificar si el usuario autenticado tiene permisos de administrador principal.

from functools import wraps
# Permite que el decorador personalizado conserve el nombre y la docstring de la vista original.
# Es una buena práctica al crear decoradores en Python.

def solo_admin_principal(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            admin = Administrador.objects.get(correo=request.user.username)
            if not admin.es_principal:
                return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        except Administrador.DoesNotExist:
            return HttpResponseForbidden("Acceso no autorizado.")
        return view_func(request, *args, **kwargs)
    return wrapper

# nor permite manejar la proteccion de las rutas 


