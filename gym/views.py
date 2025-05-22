from django.shortcuts import render,redirect
from .models import Usuario,Rol,Usuario_rol,TipoMembresia,Membresia
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,'gym/index.html')

def usuario(request):
    busqueda = request.GET.get('buscar', '')
    filtro_membresia = request.GET.get('tipo', '')

    usuarios = Usuario.objects.filter(
        Q(username__icontains=busqueda)
    )

    datos = []
    for usuario in usuarios:
        membresia = Membresia.objects.filter(mem_usuario=usuario).select_related('mem_tipo').order_by('-mem_fecha_inicio').first()

        # Aplicar filtro de membresía si se especificó
        if filtro_membresia:
            if not membresia or membresia.mem_tipo.tm_nombre.lower() != filtro_membresia.lower():
                continue

        datos.append({
            'usuario': usuario,
            'membresia': membresia
        })

    return render(request, 'gym/usuario.html', {
        'datos': datos,
        'busqueda': busqueda,
        'filtro_membresia': filtro_membresia,
    })

def crearUsuario(request):
    roles = Rol.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        nombre = request.POST['usuario_nombre']
        apellidos = request.POST['usuario_apellidos']
        email = request.POST['usuario_email']
        password = request.POST['usuario_password']
        rol_id = request.POST['ur_rolId']
        status = request.POST.get('usuario_status', 'True') == 'True'
        imagen = request.FILES.get('usuario_imagen')

        # Crear usuario
        usuario = Usuario.objects.create(
            username=username,
            usuario_nombre=nombre,
            usuario_apellidos=apellidos,
            usuario_email=email,
            usuario_password=password,  
            usuario_status=status,
            usuario_imagen=imagen
        )

        
        Usuario_rol.objects.create(
            ur_username=usuario,
            ur_rolId=Rol.objects.get(pk=rol_id)
        )

        return redirect('/usuario/')
    context = {
        'roles':roles
    }

    return render(request,'gym/crearUsuario.html',context)

def editar_usuario(request, username):
    usuario = get_object_or_404(Usuario, pk=username)
    roles = Rol.objects.all()

    try:
        usuario_rol = Usuario_rol.objects.get(ur_username=usuario)
        rol_actual = usuario_rol.ur_rolId.pk
    except Usuario_rol.DoesNotExist:
        usuario_rol = None
        rol_actual = None

    if request.method == 'POST':
        usuario.usuario_nombre = request.POST['usuario_nombre']
        usuario.usuario_apellidos = request.POST['usuario_apellidos']
        usuario.usuario_email = request.POST['usuario_email']
        usuario.usuario_status = request.POST.get('usuario_status', 'True') == 'True'

        if 'usuario_imagen' in request.FILES:
            usuario.usuario_imagen = request.FILES['usuario_imagen']

        usuario.save()

        nuevo_rol_id = request.POST['ur_rolId']
        nuevo_rol = Rol.objects.get(pk=nuevo_rol_id)

        if usuario_rol:
            usuario_rol.ur_rolId = nuevo_rol
            usuario_rol.save()
        else:
            Usuario_rol.objects.create(ur_username=usuario, ur_rolId=nuevo_rol)

        return redirect('/usuario/')

    context = {
        'usuario': usuario,
        'roles': roles,
        'rol_actual': rol_actual,
    }

    return render(request, 'gym/editar_usuario.html', context)

def eliminar_usuario(request, username):
    usuario = get_object_or_404(Usuario, pk=username)
    usuario.delete()
    return redirect('/usuario/')

"""MEMBRESIAS"""

def membresia(request):
    membresias = Membresia.objects.select_related('mem_tipo', 'mem_usuario').all().order_by('-mem_fecha_inicio')
    context = {
        'membresias': membresias
    }
    return render(request, 'gym/membresia.html', context)


def crear_membresia(request):
    if request.method == 'POST':
        tipo_id = request.POST.get('mem_tipo')
        usuario_id = request.POST.get('mem_usuario')

        try:
            tipo = TipoMembresia.objects.get(pk=tipo_id)
            usuario = Usuario.objects.get(pk=usuario_id)
        except (TipoMembresia.DoesNotExist, Usuario.DoesNotExist):
            messages.error(request, 'Datos inválidos.')
            return redirect('crear_membresia')

        # Validación 1: Usuario debe estar activo
        if not usuario.usuario_status:
            messages.error(request, f'El usuario "{usuario.username}" no está activo.')
            return redirect('crear_membresia')

        # Validación 2: Usuario no debe tener una membresía activa
        membresia_activa = Membresia.objects.filter(mem_usuario=usuario, mem_status=True).first()
        if membresia_activa:
            messages.error(request, f'El usuario "{usuario.username}" ya tiene una membresía activa.')
            return redirect('crear_membresia')

        # Si pasa las validaciones, crear membresía
        Membresia.objects.create(
            mem_tipo=tipo,
            mem_usuario=usuario
        )

        messages.success(request, f'Membresía asignada correctamente a {usuario.usuario_nombre}.')
        return redirect('membresia')

    tipos = TipoMembresia.objects.all()
    usuarios = Usuario.objects.filter(usuario_status=True)  # Solo mostrar usuarios activos en el formulario
    context = {
        'tipos': tipos,
        'usuarios': usuarios
    }
    return render(request, 'gym/crear_membresia.html', context)