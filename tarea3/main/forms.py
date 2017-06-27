from django import forms
from .models import *

tiposUsuario = (
    (0, 'Elige tipo de usuario'),
    (1, 'Fijo'),
    (2, 'Ambulante'),
    (3, 'Consumidor'),)

formasDePagoLista = (
        (None, 'Formas de pago'),
        (1, 'Efectivo'),
        (2, 'Tarjeta de Crédito'),
        (3, 'Tarjeta de Débito'),
        (4, 'Tarjeta Junaeb'),
    )

listaCategorias = (
    (None, 'Elige categoria'),
    (1, 'Snacks'),
    (2, 'Almuerzos'),
    )


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpBaseForm(forms.Form):
    nombre = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=False)
    avatar = forms.ImageField(max_length=50, required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))
    horaIni = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'validate'}))
    horaFin = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'validate'}))


class SignUpForm(SignUpBaseForm):
    nombre = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=150, required=True, widget=forms.PasswordInput())
    tipo = forms.ChoiceField(required=False, choices=tiposUsuario, widget=forms.Select(attrs={'class': 'multiple'}))
    lat = forms.DecimalField(max_digits=8, decimal_places=4, required=False)
    lng = forms.DecimalField(max_digits=8, decimal_places=4,  required=False)
    horaIni = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'validate'}))
    horaFin = forms.TimeField(required=False, widget=forms.TimeInput(attrs={'type': 'time', 'class': 'validate'}))


class ItemForm(forms.Form):
    nombre = forms.CharField(max_length=200, required=True)
    categorias = forms.ChoiceField(required=False, choices=listaCategorias)
    descripcion = forms.CharField(max_length=400, required=True)
    stock = forms.IntegerField(required=True)
    precio = forms.IntegerField(required=True)
    avatar = forms.CharField(required=False, max_length=50)
    imagen = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'dropify'}))
