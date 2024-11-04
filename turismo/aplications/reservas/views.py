from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from .forms import LoginForm,ClienteRegistroForm,PqrsForm,ActivosForm,FechasForm,ReservaForm
from django.contrib.auth.hashers import check_password

from django.urls import reverse_lazy, reverse
from.models import PaqueteTuristico,FechasReserva,Cliente,Reserva,Pqrs

from django.views import View
from django.contrib.auth.models import User, Group


# views.py

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView


#Reportes por fechas 
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.db.models import Count, Sum, F
from datetime import timedelta,datetime
from django_countries.fields import Country
from django.utils.timezone import now
from openpyxl import Workbook

#Formulario para las PQRS
import pandas as pd
from calendar import month_name

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirigir según el grupo del usuario
                    if user.groups.filter(name='Administradores').exists():
                        return redirect('panelPadre')
                    elif user.groups.filter(name='Clientes').exists():
                        return redirect('panelCliente')
                    else:
                        return HttpResponse('Usuario no pertenece a ningún grupo válido')

                else:
                    form.add_error(None, 'Usuario inactivo')
            else:
                form.add_error(None, 'El nombre de usuario o la contraseña son incorrectos')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def panelPadre(request):
    return graficaClientePaisMes(request)
    # return informe_clientes_pais_mes(request, 'reportes/graficaClientePais.html', {'section': 'panelPadre'})
    #return render(request, 'Panel/panelPadre.html', {'section': 'panelPadre'})
    

def verificar_cliente(request, paquete_id, fecha_id):
    paquete = get_object_or_404(PaqueteTuristico, id=paquete_id)
    fecha_reserva = get_object_or_404(FechasReserva, id=fecha_id)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                # Obtener el cliente autenticado
                cliente = Cliente.objects.get(user=user)
                
                # Crear una nueva reserva para este cliente, paquete y fecha
                Reserva.objects.create(
                    cliente=cliente,
                    paquete=paquete,
                    fecha_reserva=fecha_reserva
                )
                
                # Redirigir al panel del cliente después de guardar la reserva
                return redirect('panelCliente')  # Redirect to the client panel
            else:
                form.add_error(None, 'El nombre de usuario o la contraseña son incorrectos')
    else:
        form = LoginForm()

    return render(request, 'verificar_cliente.html', {'form': form, 'paquete': paquete, 'fecha_reserva': fecha_reserva})


def registrar_cliente(request, paquete_id, fecha_id):
    paquete = get_object_or_404(PaqueteTuristico, id=paquete_id)
    fecha_reserva = get_object_or_404(FechasReserva, id=fecha_id)

    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            user = form.save(paquete=paquete)  # Pasar el paquete al método save()
            cliente = Cliente.objects.get(user=user)  # Obtener la instancia de Cliente correspondiente al usuario
            
            # Guardar reserva con el cliente correcto
            Reserva.objects.create(cliente=cliente, paquete=paquete, fecha_reserva=fecha_reserva)
            
            login(request, user)
            return redirect('panelCliente')  # Redirect to a view after successful registration
    else:
        form = ClienteRegistroForm()
    return render(request, 'registroCliente.html', {'form': form,'paquete': paquete,'fecha_reserva': fecha_reserva})



@login_required
def panelCliente(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    reservas = Reserva.objects.filter(cliente=cliente).order_by('-fechaReserva') 

    # Agregar paginador para mostrar 5 reservas por página
    paginator = Paginator(reservas, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Panel/indexCliente.html', {'page_obj': page_obj})


def reserva_detail(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'detalle_reserva.html', {'reserva': reserva})    

def logout_view(request):
    logout(request)
    next_page = request.GET.get('next')
    if next_page:
        return redirect(next_page)
    return redirect('login')   

#metodo de Asignar Fechas y cantidad de personas 
def fechas_reserva(request, paquete_id):
    paquete = get_object_or_404(PaqueteTuristico, id=paquete_id)
    fecha = None

    if request.method == 'POST':
        form = FechasForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            # Asignar los valores de días y noches seleccionados a la reserva
            reserva.dias_seleccionados = request.POST.get('dias_seleccionados')
            reserva.noches_seleccionadas = request.POST.get('noches_seleccionadas')
            
            reserva.paquete = paquete
            reserva.save()
            fecha_id = reserva.id  # Corrected this line
            return redirect('verificar_cliente', paquete_id=paquete.id, fecha_id=fecha_id)
    else:
        form = FechasForm()
    return render(request, 'fechasReserva.html', {'paquete': paquete, 'fecha': fecha,'form': form})

#Se crea la vista para el formulario de PQRS
def pqrsCliente(request):
    if request.method == 'POST':
        form = PqrsForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en la base de datos
            return redirect('pqrs_success')  # Redirige a una página de éxito
    else:
        form = PqrsForm()
    
    return render(request, 'home/pqrs_form.html', {'form': form})
def pqrs_success_view(request):
    return render(request, 'home/pqrs_success.html')



class HomeView(TemplateView):
    template_name = "home/home.html"

class RestauranteView(TemplateView):
    template_name = "home/Restaurante.html"

class FooterView(TemplateView):
    template_name = "home/footer.html"

class NosotrosView(TemplateView):
    template_name = "home/nosotros.html"    

class  ContactoView(TemplateView):
    template_name = "home/contactanos.html"

class InformacionView(TemplateView):
    template_name  = "home/informacion.html"


class PanelView(TemplateView):
    template_name = "index.html"

class PanelClienteView(TemplateView):
    template_name = "Panel/indexCliente.html"    

class PruebaView(TemplateView):
    template_name = "home.html"

@method_decorator(login_required, name='dispatch')
class PqrsListView(ListView):
    model = Pqrs
    template_name = "reportes/reportePqrs.html"
    context_object_name ="datos"
    login_url = '/login/'    

@method_decorator(login_required, name='dispatch')
class paqueteCreateView(CreateView):
    model = PaqueteTuristico
    template_name = "crearPaquete.html"
    forms_class = ActivosForm
    fields = ['nombre','descripcion','incluye','no_incluye','imagenUno','imagenDos','imagenTres']
    success_url= "paquetelistar"
    def get_success_url(self):
        return reverse('paquetelistar')
    login_url = '/login/'

@method_decorator(login_required, name='dispatch')
class PaqueteListView(ListView):
    model = PaqueteTuristico
    template_name = "listarPaquetes.html"
    context_object_name ="datos"
    login_url = '/login/'


class PaqueteListarUsuarioListView(ListView):
    model = PaqueteTuristico
    template_name = "listarPaquetesUsuarios.html"
    context_object_name ="paquetes"    

class PaqueteListarUsuarioMejoradoListView(ListView):
    model = PaqueteTuristico
    template_name = "listar_paquetesMejorado.html"
    context_object_name ="paquetes"     



@method_decorator(login_required, name='dispatch')
class PaqueteUpdateView(UpdateView):
    model = PaqueteTuristico
    template_name = "actualizarPaquete.html"
    fields = ['nombre','descripcion','incluye','no_incluye','imagenUno','imagenDos','imagenTres']
    context_object_name = 'datos'
    success_url = 'paquetelistar'
    def get_success_url(self):
        return reverse('paquetelistar')
    login_url = '/login/'

@method_decorator(login_required, name='dispatch')
class PaqueteDeleteView(DeleteView):
    model = PaqueteTuristico
    template_name = 'eliminarPaquete.html'  # Plantilla de confirmación
    success_url = reverse_lazy('paquetelistar')  # Redirigir al listado después de eliminar    

@method_decorator(login_required, name='dispatch')
class ReporteListView(ListView):
    model = Reserva
    template_name = "reportes/reporte.html"
    context_object_name ="reportes"
    login_url = '/login/'


@method_decorator(login_required, name='dispatch')
class CLienteRegistradoListView(ListView):
    model = Cliente
    template_name = "reportes/reporteClienteRegistrado.html"
    context_object_name ="reportes"
    login_url = '/login/'

@login_required
def reporteReservaFecha(request):
    reservas = Reserva.objects.select_related('cliente', 'paquete', 'fecha_reserva').all()
    
    # Diccionario para guardar el informe
    reporte = {}

    for reserva in reservas:
        fecha_inicio = reserva.fecha_reserva.fechaInicio
        fecha_final = reserva.fecha_reserva.fechaFinal
        cliente_nombre = reserva.cliente.nombre
        cliente_apellidos = reserva.cliente.apellidos
        paquete_nombre = reserva.paquete.nombre
        clientes_reserva = reserva.fecha_reserva.personas  # Asegúrate de tener este campo que refleje el número de personas por reserva
        dias_seleccionados = (fecha_final - fecha_inicio).days + 1  # Días totales seleccionados
        noches_seleccionadas = dias_seleccionados - 1  # Noches totales

        # Recorremos las fechas del rango de la reserva
        for dia in range(dias_seleccionados):
            fecha = fecha_inicio + timedelta(days=dia)

            if fecha not in reporte:
                reporte[fecha] = {
                    'clientes_total': 0,
                    'clientes_estadias': 0,
                    'paquetes': {}
                }
            
            # Actualizamos los totales de clientes por día con la cantidad de personas en la reserva
            reporte[fecha]['clientes_total'] += clientes_reserva  # Aquí sumamos el total de personas de la reserva

            # Si el cliente pasa la noche, se cuenta en el primer día
            if dia < noches_seleccionadas:
                reporte[fecha]['clientes_estadias'] += clientes_reserva  # También sumamos el total de personas que se quedan por noche

            # Por paquete turístico
            if paquete_nombre not in reporte[fecha]['paquetes']:
                reporte[fecha]['paquetes'][paquete_nombre] = {
                    'clientes_total': 0,
                    'clientes_estadias': 0,
                    'cliente_nombre': cliente_nombre,
                    'cliente_apellidos': cliente_apellidos  
                }

            # Actualizamos por paquete turístico
            reporte[fecha]['paquetes'][paquete_nombre]['clientes_total'] += clientes_reserva
            if dia < noches_seleccionadas:
                reporte[fecha]['paquetes'][paquete_nombre]['clientes_estadias'] += clientes_reserva

    # Ordenar las fechas para mejor visualización en el template
    reporte_ordenado = dict(sorted(reporte.items()))

    return render(request, 'reportes/reporteReservasMes.html', {'reporte': reporte_ordenado})


####-----------FUNCION DESCARGAR EXCEL INFORME PAQUETES RESERVADOS-------#######
@login_required
def reporteExcelPaquetes(request):
    # Crear un libro de trabajo y agregar una hoja de trabajo
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Informe de Reservas'

    # Agregar encabezados
    worksheet.append(['Nro', 'Fecha Reserva', 'Hora Reserva', 'Tipo Documento', 
                      'Número Documento', 'Nombres', 'Apellidos', 'Teléfono', 
                      'Fecha Inicio', 'Fecha Final', 'Cantidad Viajeros', 
                      'Nacionalidad', 'Paquete Seleccionado', 'Dias Seleccionados', 'Noches Estadia'])

    # Obtener las reservas (ajusta la consulta según tus necesidades)
    reportes = Reserva.objects.select_related('cliente', 'paquete', 'fecha_reserva').all()

    # Agregar datos a la hoja de trabajo
    for reporte in reportes:
        worksheet.append([
            reporte.id,
            reporte.fechaReserva,
            reporte.horaReserva,
            reporte.cliente.tipo_documento,
            reporte.cliente.numero_documento,
            reporte.cliente.nombre,
            reporte.cliente.apellidos,
            reporte.cliente.telefono,
            reporte.fecha_reserva.fechaInicio,
            reporte.fecha_reserva.fechaFinal,
            reporte.fecha_reserva.personas,
            reporte.cliente.get_nacionalidad_display(),
            reporte.paquete.nombre,
            reporte.fecha_reserva.dias_seleccionados,
            reporte.fecha_reserva.noches_seleccionadas
     
        ])

    # Crear el objeto HttpResponse con el encabezado apropiado para Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=informe_reservas.xlsx'

    # Guardar el libro de trabajo en la respuesta
    workbook.save(response)
    return response

@login_required
#----------------------FUNCION DESCARR INFORME CLIENTES POR PAIS----------------######
def reporteExcel_ClientePais(request):
    # Crear un libro de trabajo y agregar una hoja de trabajo
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Reporte de Clientes por País'

    # Agregar encabezados
    worksheet.append(['Mes', 'País', 'Cantidad'])

    # Suponiendo que quieres agrupar por mes y nacionalidad
    clientes_por_mes = (
        Cliente.objects
        .values('nacionalidad', 'fecha_registro__month')  # Agrupar por nacionalidad y mes
        .annotate(total_clientes=Count('id'))  # Contar el total de clientes en cada grupo
    )

    # Agregar datos a la hoja de trabajo
    for cliente in clientes_por_mes:
        month = cliente['fecha_registro__month']  # Extraer el mes
        month_name_str = get_month_name(month)  # Convertir el número del mes en nombre del mes

        # Obtener el nombre completo de la nacionalidad
        # Crear un objeto Cliente temporal para obtener la representación de la nacionalidad
        temp_cliente = Cliente(nacionalidad=cliente['nacionalidad'])
        nombre_pais = temp_cliente.get_nacionalidad_display()

        worksheet.append([
            month_name_str,  # Convertir el número del mes en nombre del mes
            nombre_pais,     # Nombre completo del país
            cliente['total_clientes'],
        ])

    # Crear el objeto HttpResponse con el encabezado apropiado para Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=clientes_por_pais.xlsx'

    # Guardar el libro de trabajo en la respuesta
    workbook.save(response)
    return response

def get_month_name(month_number):
    """Función auxiliar para convertir el número del mes en el nombre del mes."""
    return month_name[month_number]


@login_required
def graficaClientePaisMes(request):
    mes_seleccionado = int(request.GET.get('mes', datetime.now().month))  
    anio_seleccionado = int(request.GET.get('anio', datetime.now().year))  

    # Filtrar y ordenar clientes por mes, año y número total de clientes de mayor a menor
    clientes_filtrados = Cliente.objects.filter(
        fecha_registro__month=mes_seleccionado,
        fecha_registro__year=anio_seleccionado
    ).values('nacionalidad').annotate(total=Count('nacionalidad')).order_by('-total')

    # Datos para la gráfica y la tabla
    data_grafico = []
    total_mensual = 0
    for cliente in clientes_filtrados:
        nombre_pais = Country(cliente['nacionalidad']).name  # Convertir código ISO a nombre de país
        data_grafico.append({
            'name': nombre_pais,
            'value': cliente['total']
        })
        total_mensual += cliente['total']

    # Crear la lista de meses y años
    meses = list(range(1, 13))
    anios = list(range(2024, 2031))

    contexto = {
        'data_grafico': data_grafico,
        'mes_seleccionado': mes_seleccionado,
        'anio_seleccionado': anio_seleccionado,
        'total_mensual': total_mensual,
        'meses': meses,
        'anios': anios,
    }
    return render(request, 'reportes/graficaClientePais.html', contexto)

@login_required
def graficaReservasPaquete(request):
    # Obtener el mes y año actual
    today = now().date()
    mes_actual = today.month
    año_actual = today.year

    # Obtener el mes y año seleccionados por el usuario, si se proporciona
    mes_seleccionado = int(request.GET.get('mes', mes_actual))
    año_seleccionado = int(request.GET.get('año', año_actual))

    # Obtener el número de reservas por paquete turístico para el mes y el año seleccionado
    reservas = (Reserva.objects.filter(fechaReserva__year=año_seleccionado, fechaReserva__month=mes_seleccionado)
                .values('paquete__nombre')
                .annotate(reserva_count=Count('id')))

    # Convertir los datos en listas de nombres de paquetes y cantidades de reservas
    nombres_paquetes = [reserva['paquete__nombre'] for reserva in reservas]
    cantidad_reservas = [reserva['reserva_count'] for reserva in reservas]

    # Calcular el total de todas las reservas
    total_reservas = sum(cantidad_reservas)

    # Listas de meses y años para los selects en el formulario
    meses = list(range(1, 13))
    años = list(range(2020, 2031))

    # Pasar los datos al template
    context = {
        'nombres_paquetes': nombres_paquetes,
        'cantidad_reservas': cantidad_reservas,
        'mes_actual': mes_seleccionado,
        'año_actual': año_seleccionado,
        'meses': meses,
        'años': años,
        'total_reservas': total_reservas,  # Añadimos el total al contexto
    }
    return render(request, 'reportes/graficaReservasPaquete.html', context)



