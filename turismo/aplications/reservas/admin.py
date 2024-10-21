from django.contrib import admin

# Register your models here.
from.models import PaqueteTuristico,FechasReserva,Cliente,Reserva,Pqrs


admin.site.register(PaqueteTuristico)
admin.site.register(Cliente)
admin.site.register(FechasReserva)
admin.site.register(Reserva)
admin.site.register(Pqrs)




# admin.site.register(Reserva)

