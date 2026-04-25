from django.shortcuts import redirect

def rol_requerido(nombre_rol):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            try:
                if request.user.usuario.id_rol.nombre_rol == nombre_rol:
                    return view_func(request, *args, **kwargs)
            except:
                pass

            return redirect('inicio')
        return wrapper
    return decorator