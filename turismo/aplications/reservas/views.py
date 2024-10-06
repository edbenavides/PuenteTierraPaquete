from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import LoginForm,ClienteRegistroForm, PQRSForm
from django.contrib.auth.hashers import check_password

from django.urls import reverse_lazy, reverse
from.models import PaqueteTuristico,FechasReserva,Cliente,Reserva
from.forms import ActivosForm,FechasForm,ReservaForm
from django.views import View
from django.contrib.auth.models import User, Group

# views.py

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic import TemplateView,CreateView,ListView,UpdateView,DeleteView


#Reportes por fechas 
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.db.models import Count, Sum
from datetime import timedelta,datetime
from django_countries.fields import Country

#Formulario para las PQRS
from.forms import PQRSForm




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
    return render(request, 'index.html', {'section': 'panelPadre'})
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
    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'Panel/PanelCliente.html', {'reservas': reservas})



# def reserva_detail(request, paquete_id, fecha_id):
#     paquete = get_object_or_404(PaqueteTuristico, id=paquete_id)
#     fecha_reserva = get_object_or_404(FechasReserva, id=fecha_id)
#     cliente = request.user  # Información del cliente registrado

#     return render(request, 'detalle_reserva.html', {'paquete': paquete,'fecha_reserva': fecha_reserva,'cliente': cliente})    



def reserva_detail(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'detalle_reserva.html', {'reserva': reserva})    




# def registrar_cliente(request):
#     if request.method == 'POST':
#         form = ClienteRegistroForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             client_group = Group.objects.get(name='Clientes')
#             user.groups.add(client_group)

#             login(request, user)
#             return redirect('login')  # Cambia a la URL de tu elección
#     else:
#         form = ClienteRegistroForm()

#     return render(request, 'registroCliente.html', {'form': form})    




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
             reserva.paquete = paquete
             reserva.save()
             fecha_id = reserva.id  # Corrected this line
             return redirect('verificar_cliente', paquete_id=paquete.id, fecha_id=fecha_id)
     else:
         form = FechasForm()
     return render(request, 'fechasReserva.html', {'paquete': paquete, 'fecha': fecha,'form': form})

#Se crea la vista para el formulario de PQRS
def PQRS(request):
    if request.method == 'POST':
        form = PQRSForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en la base de datos
            return redirect('pqrs_success')  # Redirige a una página de éxito
    else:
        form = PQRSForm()
    
    return render(request, 'home/pqrs_form.html', {'form': form})


def pqrs_success_view(request):
    return render(request, 'home/pqrs_success.html')



class HomeView(TemplateView):
    template_name = "home/home.html"

class RestauranteView(TemplateView):
    template_name = "home/Restaurante.html"



class PanelView(TemplateView):
    template_name = "index.html"

class PruebaView(TemplateView):
    template_name = "home.html"



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

# Vista para mostrar el informe de reservas por mes
def reservas_informe(request):
    # Agrupar reservas por mes y paquete, y contar el número total de reservas
    reservas_por_mes = (
        Reserva.objects
        .values('fechaReserva__year', 'fechaReserva__month', 'paquete__nombre')  # Agrupar por mes y paquete
        .annotate(total_reservas=Count('id'))  # Contar las reservas por paquete
        .order_by('fechaReserva__year', 'fechaReserva__month', '-total_reservas')  # Ordenar por mes y por número de reservas
    )
    
    # Obtener el total de reservas por mes
    total_reservas_por_mes = (
        Reserva.objects
        .values('fechaReserva__year', 'fechaReserva__month')  # Agrupar solo por mes
        .annotate(total_reservas=Count('id'))  # Contar las reservas totales por mes
        .order_by('fechaReserva__year', 'fechaReserva__month')  # Ordenar por mes
    )

    # Estructura de datos para facilitar la presentación
    datos_por_mes = {}
    for reserva in reservas_por_mes:
        year_month = f"{reserva['fechaReserva__year']}-{reserva['fechaReserva__month']:02d}"
        if year_month not in datos_por_mes:
            datos_por_mes[year_month] = {
                'paquetes': [],
                'total_reservas_mes': next(
                    (item['total_reservas'] for item in total_reservas_por_mes if item['fechaReserva__year'] == reserva['fechaReserva__year'] and item['fechaReserva__month'] == reserva['fechaReserva__month']),
                    0
                ),
            }
        datos_por_mes[year_month]['paquetes'].append({
            'paquete': reserva['paquete__nombre'],
            'total_reservas': reserva['total_reservas'],
        })

    context = {
        'datos_por_mes': datos_por_mes,
    }
    
    return render(request, 'reportes/reporteMes.html', context)  

def clientesPaisPorMes(request):
    # Agrupamos los clientes por mes y nacionalidad
     # Agrupamos los clientes por mes y nacionalidad
    clientes_por_mes_raw = (
        Cliente.objects
        .annotate(mes=TruncMonth('fecha_registro'))  # Agrupamos por mes
        .values('mes', 'nacionalidad')
        .annotate(total_clientes=Count('id'))
        .order_by('mes', 'nacionalidad')
    )

    # Convertimos los códigos de país a nombres legibles
    clientes_por_mes = []
    for cliente in clientes_por_mes_raw:
        cliente['nacionalidad'] = Country(cliente['nacionalidad']).name  # Convierte siglas a nombre del país
        clientes_por_mes.append(cliente)
    
    return render(request, 'reportes/reporteClientesPais.html', {'clientes_por_mes': clientes_por_mes})
