from django.shortcuts import render,redirect
from .models import Usuario,Rol,Usuario_rol,\
TipoMembresia,Membresia,EntrenadorInfo,UsuarioEntrenador,AvanceFisico
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
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
    tipos = TipoMembresia.objects.all()
    usuarios = Usuario.objects.filter(usuario_status=True)

    if request.method == 'POST':
        # Filtro por nombre o apellido
        if request.POST.get('filtrar'):
            filtro = request.POST.get('filtro_usuario', '').strip()
            usuarios = usuarios.filter(
                Q(usuario_nombre__icontains=filtro) |
                Q(usuario_apellidos__icontains=filtro)
            )
        else:
            tipo_id = request.POST.get('mem_tipo')
            usuario_id = request.POST.get('mem_usuario')

            try:
                tipo = TipoMembresia.objects.get(pk=tipo_id)
                usuario = Usuario.objects.get(pk=usuario_id)
            except (TipoMembresia.DoesNotExist, Usuario.DoesNotExist):
                messages.error(request, 'Datos inválidos.')
                return redirect('crear_membresia')

            # Validación de usuario
            if not usuario.usuario_status:
                messages.error(request, f'El usuario "{usuario.username}" no está activo.')
                return redirect('crear_membresia')

            membresia_activa = Membresia.objects.filter(mem_usuario=usuario, mem_status=True).first()
            if membresia_activa:
                messages.error(request, f'El usuario "{usuario.username}" ya tiene una membresía activa.')
                return redirect('crear_membresia')

            # Crear membresía
            Membresia.objects.create(mem_tipo=tipo, mem_usuario=usuario)
            messages.success(request, f'Membresía asignada correctamente a {usuario.usuario_nombre}.')
            return redirect('membresia')

    context = {
        'tipos': tipos,
        'usuarios': usuarios
    }
    return render(request, 'gym/crear_membresia.html', context)


"""ENTRENADORES"""
from .models import Usuario, Usuario_rol, EntrenadorInfo

def lista_entrenadores(request):
    entrenadores = Usuario.objects.filter(
        usuario_status=True,
        usuario_rol__ur_rolId=2  # ID del rol "entrenador"
    ).distinct()

    
    for entrenador in entrenadores:
        entrenador.info = EntrenadorInfo.objects.filter(entrenador=entrenador).first()

    return render(request, 'gym/entrenadores.html', {'entrenadores': entrenadores})

def crear_info_entrenador(request, username):
    try:
        usuario = Usuario.objects.get(username=username)
        if not Usuario_rol.objects.filter(ur_username=usuario, ur_rolId=2).exists():
            messages.error(request, "Este usuario no tiene el rol de entrenador.")
            return redirect('entrenadores')
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('entrenadores')

    
    info_existente = EntrenadorInfo.objects.filter(entrenador=usuario).first()
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    dias_seleccionados = []

    if info_existente:
        dias_seleccionados = info_existente.dias_disponibles.split(',')

    if request.method == 'POST':
        especialidad = request.POST.get('especialidad')
        dias = request.POST.getlist('dias') 
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        descripcion = request.POST.get('descripcion')

        EntrenadorInfo.objects.update_or_create(
            entrenador=usuario,
            defaults={
                'especialidad': especialidad,
                'dias_disponibles': ",".join(dias),
                'hora_inicio': hora_inicio,
                'hora_fin': hora_fin,
                'descripcion': descripcion
            }
        )
        messages.success(request, "Información del entrenador guardada correctamente.")
        return redirect('entrenadores')

    context = {
        'usuario': usuario,
        'info': info_existente,
        'dias_semana': dias_semana,
        'dias_seleccionados': dias_seleccionados

    }
    return render(request, 'gym/entrenador_info.html',context)


def asignar_entrenador(request):
    clientes = Usuario.objects.filter(usuario_status=True, usuario_rol__ur_rolId=1).distinct()
    entrenadores = Usuario.objects.filter(usuario_status=True, usuario_rol__ur_rolId=2).distinct()

    if request.method == 'POST':
        cliente_username    = request.POST.get('cliente')
        entrenador_username = request.POST.get('entrenador')

        try:
            cliente    = Usuario.objects.get(username=cliente_username)
            entrenador = Usuario.objects.get(username=entrenador_username)
        except Usuario.DoesNotExist:
            messages.error(request, "Datos de usuario incorrectos.")
            return redirect('asignar_entrenador')

        # ─── VALIDACIÓN DE MEMBRESÍA ───────────────────────────────────────────────
        hoy = timezone.now().date()
        membresia_activa = (
            Membresia.objects.filter(
                mem_usuario=cliente,
                mem_status=True,                    
                mem_fecha_fin__gte=hoy              
            )
            .exclude(mem_tipo__tm_nombre__iexact='Individual') 
            .first()
        )

        if not membresia_activa:
            messages.error(request, "El cliente no tiene una membresía activa válida para asignar entrenador.")
            return redirect('asignar_entrenador')
        # ──────────────────────────────────────────────────────────────────────────

        UsuarioEntrenador.objects.update_or_create(
            ue_cliente=cliente,
            defaults={'ue_entrenador': entrenador}
        )
        messages.success(request, f"{cliente.usuario_nombre} fue asignado a {entrenador.usuario_nombre}.")
        return redirect('asignar_entrenador')

    asignaciones = UsuarioEntrenador.objects.select_related('ue_cliente', 'ue_entrenador')

    context = {
         'clientes': clientes,
        'entrenadores': entrenadores,
        'asignaciones': asignaciones
    }
    return render(request, 'gym/asignar_entrenador.html',context)

def eliminar_asignacion(request, cliente_username):
    try:
        cliente = Usuario.objects.get(username=cliente_username)
        asignacion = UsuarioEntrenador.objects.get(ue_cliente=cliente)
        asignacion.delete()
        messages.success(request, f"Asignación del cliente {cliente.usuario_nombre} fue cancelada.")
    except Usuario.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
    except UsuarioEntrenador.DoesNotExist:
        messages.error(request, "No se encontró asignación para este cliente.")

    return redirect('asignar_entrenador')

"""AVANCE FISICO"""
def avances_fisicos_inicio(request):
    clientes = Usuario.objects.filter(usuario_status=True, usuario_rol__ur_rolId=1)
    context = {
        'clientes': clientes
    }
    return render(request, 'gym/avances_inicio.html', context)


def registrar_avance_fisico(request):
    clientes = Usuario.objects.filter(usuario_status=True, usuario_rol__ur_rolId=1)
    entrenadores = Usuario.objects.filter(usuario_status=True, usuario_rol__ur_rolId=2)

    if request.method == 'POST':
        cliente_username    = request.POST.get('cliente')
        entrenador_username = request.POST.get('entrenador')

        try:
            cliente    = Usuario.objects.get(username=cliente_username)
            entrenador = Usuario.objects.get(username=entrenador_username)
        except Usuario.DoesNotExist:
            messages.error(request, "Datos de usuario incorrectos.")
            return redirect('registrar_avance_fisico')

        # ─── VALIDACIÓN DE MEMBRESÍA ───────────────────────────────────────────────
        hoy = timezone.now().date()
        membresia_activa = (
            Membresia.objects.filter(
                mem_usuario=cliente,
                mem_status=True,
                mem_fecha_fin__gte=hoy
            )
            .exclude(mem_tipo__tm_nombre__iexact='Individual')
            .first()
        )

        if not membresia_activa:
            messages.error(request, "El cliente no tiene una membresía activa válida para registrar avances.")
            return redirect('registrar_avance_fisico')
        # ──────────────────────────────────────────────────────────────────────────

        AvanceFisico.objects.create(
            cliente    = cliente,
            entrenador = entrenador,
            fecha      = request.POST.get('fecha'),
            peso       = request.POST.get('peso'),
            estatura   = request.POST.get('estatura'),
            grasa_corporal = request.POST.get('grasa'),
            comentario = request.POST.get('comentario')
        )
        messages.success(request, "Avance físico registrado correctamente.")
        return redirect('registrar_avance_fisico')

    context = {
        'clientes': clientes,
        'entrenadores': entrenadores
    }
    return render(request, 'gym/registrar_avance.html',context)

def historial_avances_cliente(request, username):
    try:
        cliente = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
        messages.error(request, "Cliente no encontrado.")
        return redirect('asignar_entrenador')

    avances = AvanceFisico.objects.filter(cliente=cliente).order_by('-fecha')

    context = {
        'cliente': cliente,
        'avances': avances
    }
    return render(request, 'gym/historial_avances.html',context)

"""REPORTES"""
def vista_reporte_membresias_activas(request):
    return render(request, 'gym/reporte_membresias_activas.html')

def vista_reporte_membresias_por_tipo(request):
    return render(request, 'gym/reporte_membresias_por_tipo.html')



