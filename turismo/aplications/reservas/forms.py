
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms.widgets import DateInput
from django.core.exceptions import ValidationError

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from.models import PaqueteTuristico,FechasReserva,Cliente,Reserva

class LoginForm(forms.Form):
    username = forms.CharField(label='Correo', max_length=150)
    password = forms.CharField(widget=forms.PasswordInput,label='Contraseña',)

class ClienteRegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")  # Campo obligatorio
    tipo_documento = forms.ChoiceField(choices=Cliente.TIPO_DOCUMENTO_CHOICES)
    numero_documento = forms.CharField(max_length=30)
    nombre = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=15)
    nacionalidad = forms.ChoiceField(choices=CountryField().choices, widget=CountrySelectWidget())

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2','tipo_documento','numero_documento', 'nombre', 'apellidos', 'telefono','nacionalidad']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email    
        
    def save(self, commit=True,paquete=None):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['nombre']  # Save to User's first_name
        user.last_name = self.cleaned_data['apellidos']  # Save to User's last_name
        if commit:
            user.save()
            client_group = Group.objects.get(name='Clientes')
            user.groups.add(client_group)
            Cliente.objects.create(
                user=user,
                tipo_documento=self.cleaned_data['tipo_documento'],
                numero_documento=self.cleaned_data['numero_documento'],
                nombre=self.cleaned_data['nombre'],
                apellidos=self.cleaned_data['apellidos'],
                telefono=self.cleaned_data['telefono'],
                nacionalidad=self.cleaned_data['nacionalidad'],
                paquete=paquete  # Añadir el paquete aquí
                
            )
        return user    

class ActivosForm(forms.ModelForm):
    class Meta:
        model = PaqueteTuristico
        fields = ('__all__')

class FechasForm(forms.ModelForm):
    class Meta:
        model = FechasReserva
        fields = ['fechaInicio', 'fechaFinal', 'personas']
        labels = {
            'fechaInicio': 'Fecha Inicial',  # Etiqueta personalizada
            'fechaFinal': 'Fecha Final',     # Etiqueta personalizada
            'personas': 'Cantidad Personas',     # Etiqueta personalizada
        }
        widgets = {
            'fechaInicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fechaFinal': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'personas': forms.NumberInput(attrs={'min': 1, 'value': 1}),  # Establecer el valor mínimo y predeterminado en 1
            'dias_seleccionados': forms.HiddenInput(),
            'noches_seleccionadas': forms.HiddenInput(),
        
        } 
                    
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('__all__')  
      