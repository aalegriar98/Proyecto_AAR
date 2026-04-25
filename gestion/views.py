from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .forms import HerramientaForm, UsuarioForm, PrestamoForm, MantenimientoForm
from .models import Usuario, Herramienta, Prestamo, Mantenimiento
from .decorators import rol_requerido


@login_required
@rol_requerido('Administrador')
def registrar_herramienta(request):
    if request.method == 'POST':
        form = HerramientaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_herramienta')
    else:
        form = HerramientaForm()

    return render(request, 'gestion/registrar_herramienta.html', {'form': form})


@login_required
@rol_requerido('Administrador')
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrar_usuario')
    else:
        form = UsuarioForm()

    return render(request, 'gestion/registrar_usuario.html', {'form': form})


@login_required
@rol_requerido('Administrador')
def registrar_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save()
            herramienta = prestamo.id_herramienta

            if prestamo.estado_prestamo == 'Prestado':
                herramienta.estado = 'Prestado'
            elif prestamo.estado_prestamo == 'Devuelto':
                herramienta.estado = 'Disponible'

            herramienta.save()
            return redirect('registrar_prestamo')
    else:
        form = PrestamoForm()

    return render(request, 'gestion/registrar_prestamo.html', {'form': form})


@login_required
@rol_requerido('Administrador')
def editar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id_usuario=id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('editar_usuario', id=id)
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'gestion/editar_usuario.html', {'form': form})


@login_required
@rol_requerido('Administrador')
def registrar_mantenimiento(request):
    if request.method == 'POST':
        form = MantenimientoForm(request.POST)
        if form.is_valid():
            mantenimiento = form.save()
            herramienta = mantenimiento.id_herramienta
            herramienta.estado = 'En mantención'
            herramienta.save()

            return redirect('listar_mantenimientos')
    else:
        form = MantenimientoForm()

    return render(request, 'gestion/registrar_mantenimiento.html', {'form': form})


@login_required
def inicio(request):
    contexto = {
        'total_herramientas': Herramienta.objects.count(),
        'disponibles': Herramienta.objects.filter(estado='Disponible').count(),
        'prestadas': Herramienta.objects.filter(estado='Prestado').count(),
        'mantencion': Herramienta.objects.filter(estado='En mantención').count(),
        'total_prestamos': Prestamo.objects.count(),
        'total_mantenimientos': Mantenimiento.objects.count(),
    }

    return render(request, 'gestion/inicio.html', contexto)


@login_required
def listar_herramientas(request):
    herramientas = Herramienta.objects.all()
    return render(request, 'gestion/listar_herramientas.html', {'herramientas': herramientas})


@login_required
def listar_prestamos(request):
    prestamos = Prestamo.objects.all()
    return render(request, 'gestion/listar_prestamos.html', {'prestamos': prestamos})


@login_required
def herramientas_disponibles(request):
    herramientas = Herramienta.objects.filter(estado='Disponible')
    return render(request, 'gestion/herramientas_disponibles.html', {'herramientas': herramientas})


@login_required
@rol_requerido('Administrador')
def eliminar_prestamo(request, id):
    prestamo = get_object_or_404(Prestamo, id_prestamo=id)

    if request.method == 'POST':
        herramienta = prestamo.id_herramienta
        prestamo.delete()

        herramienta.estado = 'Disponible'
        herramienta.save()

        return redirect('listar_prestamos')

    return render(request, 'gestion/eliminar_prestamo.html', {'prestamo': prestamo})


@login_required
@rol_requerido('Administrador')
def cambiar_estado_herramienta(request, id):
    herramienta = get_object_or_404(Herramienta, id_herramienta=id)

    if herramienta.estado == 'Prestado':
        herramienta.estado = 'Disponible'
    elif herramienta.estado == 'Disponible':
        herramienta.estado = 'Prestado'

    herramienta.save()
    return redirect('listar_herramientas')


@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'gestion/listar_usuarios.html', {'usuarios': usuarios})


@login_required
def listar_mantenimientos(request):
    mantenimientos = Mantenimiento.objects.all()
    return render(request, 'gestion/listar_mantenimientos.html', {'mantenimientos': mantenimientos})


@login_required
@rol_requerido('Administrador')
def eliminar_mantenimiento(request, id):
    mantenimiento = get_object_or_404(Mantenimiento, id_mantenimiento=id)

    if request.method == 'POST':
        herramienta = mantenimiento.id_herramienta
        mantenimiento.delete()

        herramienta.estado = 'Disponible'
        herramienta.save()

        return redirect('listar_mantenimientos')

    return render(request, 'gestion/eliminar_mantenimiento.html', {'mantenimiento': mantenimiento})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'gestion/login.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'gestion/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def alertas_atrasos(request):
    atrasos = Prestamo.objects.filter(
        fecha_entrega_real__isnull=False,
        fecha_entrega_real__gt=F('fecha_devolucion')
    )

    return render(request, 'gestion/alertas_atrasos.html', {
        'atrasos': atrasos
    })