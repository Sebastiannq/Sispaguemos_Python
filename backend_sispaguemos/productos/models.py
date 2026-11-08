from django.db import models

# Create your models here.
class Prenda(models.Model):
    id_prenda = models.AutoField(primary_key=True)
    nombre_prend = models.CharField(max_length=150)
    descripcion_prend = models.TextField(blank=True, null=True)
    genero = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cantidad_disponible_venta = models.IntegerField(default=0)
    estado = models.CharField(max_length=50, default='Disponible')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    imagen_prend = models.TextField(blank=True, null=True)
    codigo_barras = models.CharField(max_length=25, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'prenda'
        managed = False

    def __str__(self):
        return self.nombre_prend


class Hombre(models.Model):
    id_hombre = models.AutoField(primary_key=True)
    talla = models.CharField(max_length=20)
    pecho_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cintura_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cadera_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    largo_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cantidad_talla = models.IntegerField(default=0)
    fk_id_prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, db_column='fk_id_prenda')

    class Meta:
        db_table = 'hombre'
        managed = False


class Mujer(models.Model):
    id_mujer = models.AutoField(primary_key=True)
    talla = models.CharField(max_length=20)
    busto_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cintura_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cadera_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    largo_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cantidad_talla = models.IntegerField(default=0)
    fk_id_prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, db_column='fk_id_prenda')

    class Meta:
        db_table = 'mujer'
        managed = False


class Infantil(models.Model):
    id_infantil = models.AutoField(primary_key=True)
    talla = models.CharField(max_length=20)
    edad_minima = models.IntegerField(blank=True, null=True)
    edad_maxima = models.IntegerField(blank=True, null=True)
    pecho_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cintura_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    altura_cm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    cantidad_talla = models.IntegerField(default=0)
    fk_id_prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, db_column='fk_id_prenda')

    class Meta:
        db_table = 'infantil'
        managed = False


class Stock(models.Model):
    id_stock = models.AutoField(primary_key=True)
    cantidad_actual = models.IntegerField(default=0)
    cantidad_minima = models.IntegerField(default=10)
    cantidad_maxima = models.IntegerField(default=100)
    costo_promedio = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fk_id_prenda = models.OneToOneField(Prenda, on_delete=models.CASCADE, db_column='fk_id_prenda')

    class Meta:
        db_table = 'stock'
        managed = False


class ConfiguracionPrecio(models.Model):
    id_configuracion = models.AutoField(primary_key=True)
    porcentaje_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=40.00)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'configuracion_precio'
        managed = False


class SolicitudesReposicion(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    fk_id_prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, db_column='fk_id_prenda')
    cantidad_solicitada = models.IntegerField(default=50)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, default='Pendiente')
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'solicitudes_reposicion'
        managed = False