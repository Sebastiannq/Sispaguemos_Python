from rest_framework import serializers
from .models import Usuario 

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id_usuario', 
            'nombre_usuario', # En tu frontend es primerNom, lo adaptaremos en la vista
            'apellido_usuario', # En tu frontend es primerApelli
            'correo_usuario', 
            'contrasena_usuario',
            'estado',
            'fk_id_rol'
        ]