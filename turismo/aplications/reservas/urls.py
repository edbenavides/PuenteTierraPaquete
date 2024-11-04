from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views #cargar todas las vistas de autenticacion desde las urls de mi aplicacion (nueva)
from.import views 
from .views import PaqueteListarUsuarioListView,registrar_cliente,fechas_reserva,user_login,verificar_cliente,CLienteRegistradoListView,PaqueteDeleteView,reporteExcelPaquetes,reporteExcel_ClientePais,graficaClientePaisMes,graficaReservasPaquete

# from django.urls.conf import include



urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panelPadre/', views.panelPadre, name='panelPadre'),
    path('panelCliente', views.panelCliente, name='panelCliente'),
    path('panel/', views.PanelView.as_view(),name='panelIndex'),
    path('panelIndexCliente/', views.PanelClienteView.as_view(),name='panelIndexCliente'),
    path('home/', views.PruebaView.as_view()),
    path('crea/', views.paqueteCreateView.as_view(),name='crearPaquete'),
    path('listar/', views.PaqueteListView.as_view(),name='paquetelistar'), 



    # Restablecer contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),






    # rutas credas para el home inicial y el formulario de las PQRS
    path('', views.HomeView.as_view(),name='homePrincipal'),
    path('homeRestaurante/', views.RestauranteView.as_view(),name='homeRestaurante'),
    path('pqrs_form/', views.pqrsCliente,name='pqrs_form'),
    path('pqrs_success/', views.pqrs_success_view,name='pqrs_success'),
    path('footer/', views.FooterView.as_view(), name='footer'),
    path('nosotros/', views.NosotrosView.as_view(),name='nosotros'),
    path('contactanos', views.ContactoView.as_view(),name='homecontactanos'),
    path('informacion/', views.InformacionView.as_view(),name='homemasinformacion'),



    path('listarMejorado/', views.PaqueteListarUsuarioMejoradoListView.as_view(), name='listarMejorado'),



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
    path('reporteReservasFecha/', views.reporteReservaFecha, name='reporteReservasFecha'),
     path('reportePqrs/', views.PqrsListView.as_view(),name='reportePqrs'),

    #URLS DEPORTE GRAFICAS
    path('informe-clientes/', graficaClientePaisMes, name='grafica_clientes'),
    path('reservas-grafico/', graficaReservasPaquete, name='graficaReservaPaquetes'),



    #URLS REPORTES EXCEL
    path('descargar_excel/', reporteExcelPaquetes, name='Paquetes_excel'),
    path('descarga/excelPais/', reporteExcel_ClientePais, name='clientePais_excel'),
    





]
