from django.db import models

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nom_rol = models.CharField(max_length=50) # Coincide con tu SQL

    class Meta:
        db_table = 'rol'  # Apunta a tu tabla original
        managed = False   # Evita que Django cree o borre la tabla

    def __str__(self):
        return self.nom_rol

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    apellido_usuario = models.CharField(max_length=100)
    correo_usuario = models.EmailField(unique=True)
    telefono_usuario = models.CharField(max_length=20, blank=True, null=True)
    direccion_usuario = models.CharField(max_length=200, blank=True, null=True)
    contrasena_usuario = models.CharField(max_length=255)
    
    # En tu script de SQL está como LONGBLOB, así que usamos BinaryField
    imagen_perfil = models.BinaryField(blank=True, null=True) 
    
    estado = models.CharField(max_length=20, default='Activo')
    
    fk_id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='fk_id_rol')
    
    class Meta:
        db_table = 'usuario' 
        managed = False

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido_usuario}"