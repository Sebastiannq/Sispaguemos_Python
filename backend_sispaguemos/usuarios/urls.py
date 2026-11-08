from django.urls import path
from .views import registrar_usuario, login_usuario

urlpatterns = [
    path('usuarios/registrar/', registrar_usuario),
    path('usuarios/login/', login_usuario),
]