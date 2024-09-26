from django.contrib import admin

# Register your models here.
from.models import PaqueteTuristico,FechasReserva,Cliente,Reserva


admin.site.register(PaqueteTuristico)
admin.site.register(Cliente)
admin.site.register(FechasReserva)
admin.site.register(Reserva)



# admin.site.register(Reserva)

