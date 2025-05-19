from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('carga-exploracion/', views.clase_carga_exploracion, name='clase_carga_exploracion'),
    path('ejecutar_codigo/', views.ejecutar_codigo, name='ejecutar_codigo'),
    path('tipos-fuentes-datos/', views.clase_tipos_fuentes_datos, name='clase_tipos_fuentes_datos'),
]
