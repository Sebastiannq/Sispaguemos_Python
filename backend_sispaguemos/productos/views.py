# productos/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Prenda, Stock

@api_view(['GET', 'POST'])
def gestionar_bodega(request):
    if request.method == 'GET':
        try:
            stocks = Stock.objects.all()
            data = [{
                "idStock": s.id_stock,
                "idPrenda": s.fk_id_prenda.id_prenda,
                "stockActual": s.cantidad_actual,
                "stockMinimo": s.cantidad_minima,
                "stockMaximo": s.cantidad_maxima,
                "costoPromedio": float(s.costo_promedio),
                "fechaActualizacion": s.fecha_actualizacion
            } for s in stocks]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        try:
            d = request.data
            
            prenda = Prenda.objects.create(
                codigo_barras=d.get('codigoBarras'),
                nombre_prend=d.get('nombrePrend'),
                descripcion_prend=d.get('descripcionPrend', ''),
                genero=d.get('genero', 'Hombre'),
                color=d.get('color', ''),
                precio_venta=d.get('precioVenta', 0.00),
                cantidad_disponible_venta=d.get('cantidadDisponibleVenta', 0),
                estado=d.get('estado', 'Disponible'),
                imagen_prend=d.get('imagenPrend', '')
            )

            stock = Stock.objects.create(
                cantidad_actual=d.get('stockActual', 0),
                cantidad_minima=d.get('stockMinimo', 5),
                cantidad_maxima=d.get('stockMaximo', 85),
                costo_promedio=d.get('costoPromedio', 0.00),
                fk_id_prenda=prenda
            )

            return Response({
                "mensaje": "Producto registrado en bodega con éxito", 
                "idStock": stock.id_stock,
                "idPrenda": prenda.id_prenda
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def detalle_bodega(request, pk):
    try:
        stock = Stock.objects.get(pk=pk)
        prenda = stock.fk_id_prenda
    except Stock.DoesNotExist:
        return Response({'error': 'Registro de bodega no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            d = request.data
            prenda.codigo_barras = d.get('codigoBarras', prenda.codigo_barras)
            prenda.nombre_prend = d.get('nombrePrend', prenda.nombre_prend)
            prenda.descripcion_prend = d.get('descripcionPrend', prenda.descripcion_prend)
            prenda.genero = d.get('genero', prenda.genero)
            prenda.color = d.get('color', prenda.color)
            prenda.precio_venta = d.get('precioVenta', prenda.precio_venta)
            prenda.cantidad_disponible_venta = d.get('cantidadDisponibleVenta', prenda.cantidad_disponible_venta)
            prenda.estado = d.get('estado', prenda.estado)
            if 'imagenPrend' in d:
                prenda.imagen_prend = d.get('imagenPrend')
            prenda.save()

            stock.cantidad_actual = d.get('stockActual', stock.cantidad_actual)
            stock.cantidad_minima = d.get('stockMinimo', stock.cantidad_minima)
            stock.cantidad_maxima = d.get('stockMaximo', stock.cantidad_maxima)
            stock.costo_promedio = d.get('costoPromedio', stock.costo_promedio)
            stock.save()

            return Response({"mensaje": "Bodega actualizada correctamente"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try:
            prenda.delete()
            return Response({"mensaje": "Registro eliminado con éxito"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listar_prendas(request):
    try:
        prendas = Prenda.objects.all()
        data = [{
            "idPrenda": p.id_prenda,
            "codigoBarras": p.codigo_barras,
            "nombrePrend": p.nombre_prend,
            "descripcionPrend": p.descripcion_prend,
            "genero": p.genero,
            "color": p.color,
            "precioVenta": float(p.precio_venta),
            "cantidadDisponibleVenta": p.cantidad_disponible_venta,
            "estado": p.estado,
            "imagenPrend": p.imagen_prend
        } for p in prendas]
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)