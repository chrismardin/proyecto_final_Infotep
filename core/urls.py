from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('productos/', views.productos, name='productos'),
    path('ventas/', views.ventas, name='ventas'),
    path('finanzas/', views.finanzas, name='finanzas'),
    path('inventario/', views.inventario, name='inventario'),
    path('proyecciones/', views.proyecciones, name='proyecciones'),
    path('clientes/', views.clientes, name='clientes'),
    path('empleados/', views.empleados, name='empleados'),
    path('reportes/', views.reportes, name='reportes'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path("api/procesar_venta/", views.procesar_venta, name="procesar_venta"),
    path("api/historial/guardar/", views.guardar_historial_producto, name="guardar_historial_producto"),
    path("api/historial/borrar/", views.borrar_historial_producto, name="borrar_historial_producto"),
    path("api/resetear_ventas_mes/", views.resetear_ventas_mes, name="resetear_ventas_mes"),

]