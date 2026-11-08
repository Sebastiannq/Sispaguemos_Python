from django.urls import path
from .views import listar_prendas, gestionar_bodega, detalle_bodega

urlpatterns = [
    path('prendas/', listar_prendas),
    path('bodega/', gestionar_bodega),
    path('bodega/<int:pk>/', detalle_bodega),
]