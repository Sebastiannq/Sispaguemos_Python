# usuarios/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario, Rol
from .serializers import UsuarioSerializer

@api_view(['POST'])
def registrar_usuario(request):
    data = request.data
    
    try:
        rol_cliente = Rol.objects.get(id_rol=3) 
    except Rol.DoesNotExist:
        return Response({'error': 'Rol de cliente no existe en la BD.'}, status=status.HTTP_400_BAD_REQUEST)

    nuevo_usuario = Usuario(
        nombre_usuario=f"{data.get('primerNom', '')} {data.get('segundNom', '')}".strip(),
        apellido_usuario=f"{data.get('primerApelli', '')} {data.get('segundApelli', '')}".strip(),
        correo_usuario=data.get('correo'),
        contrasena_usuario=make_password(data.get('contrasena')),
        estado=data.get('estado', 'Activo'),
        fk_id_rol=rol_cliente
    )
    
    if 'imagenPerfil' in data and data.get('imagenPerfil'):
        nuevo_usuario.imagen_perfil = data.get('imagenPerfil')
        
    nuevo_usuario.save()
    
    serializer = UsuarioSerializer(nuevo_usuario)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_usuario(request):
    data = request.data
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    
    try:
        usuario = Usuario.objects.get(correo_usuario=correo)
        if check_password(contrasena, usuario.contrasena_usuario) or contrasena == usuario.contrasena_usuario:
            datos_respuesta = {
                'id': usuario.id_usuario,
                'primerNom': usuario.nombre_usuario.split()[0] if usuario.nombre_usuario else '',
                'primerApelli': usuario.apellido_usuario.split()[0] if usuario.apellido_usuario else '',
                'correo': usuario.correo_usuario,
                'rol': usuario.fk_id_rol.nom_rol,
                'imagenPerfil': usuario.imagen_perfil
            }
            return Response(datos_respuesta, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)
            
    except Usuario.DoesNotExist:
        return Response({'error': 'El correo no está registrado.'}, status=status.HTTP_404_NOT_FOUND)