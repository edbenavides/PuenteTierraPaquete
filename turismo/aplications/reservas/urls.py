from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views #cargar todas las vistas de autenticacion desde las urls de mi aplicacion (nueva)
from.import views 
from .views import PaqueteListarUsuarioListView,registrar_cliente,fechas_reserva,user_login,verificar_cliente,CLienteRegistradoListView,PaqueteDeleteView

# from django.urls.conf import include



urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panelPadre/', views.panelPadre, name='panelPadre'),
    path('panelCliente', views.panelCliente, name='panelCliente'),
    path('panel/', views.PanelView.as_view(),name='panelIndex'),
    path('home/', views.PruebaView.as_view()),
    path('crea/', views.paqueteCreateView.as_view(),name='crearPaquete'),
    path('listar/', views.PaqueteListView.as_view(),name='paquetelistar'), 


    path('homePrincipal/', views.HomeView.as_view(),name='homePrincipal'),
    path('homeRestaurante/', views.RestauranteView.as_view(),name='homeRestaurante'),


    path('listardos/', views.PaqueteListarUsuarioListView.as_view(), name='paqueteturistico_list'),
    # path('reservar/<int:paquete_id>/', views.fechas_reserva, name='fechas_reserva'),
    path('paquete/<int:paquete_id>/fechas/', fechas_reserva, name='fechas_reserva'),
    path('verificar-cliente/<int:paquete_id>/<int:fecha_id>/', verificar_cliente, name='verificar_cliente'),
    path('registrar_cliente/<int:paquete_id>/<int:fecha_id>/', registrar_cliente, name='registrar_cliente'),
    path('actualizar/<int:pk>', views.PaqueteUpdateView.as_view(),name='actualizarPaquete'),
    path('eliminar-paquete/<int:pk>/', views.PaqueteDeleteView.as_view(), name='eliminarPaquete'),

    #URLS DE REPORTES 
    path('listarReporte/', views.ReporteListView.as_view(),name='reportelistar'),
    path('reporteClienteRegistrado/', views.CLienteRegistradoListView.as_view(),name='reporteClienteRegistrado'),
    path('informe-reservas/', views.reservas_informe, name='informeMes'),
    path('reporteClientePais/', views.clientesPaisPorMes, name='reporteClientePais'),





]
