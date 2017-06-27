from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

tiposUsuario = (
    (1, 'Fijo'),
    (2, 'Ambulante'),
    (3, 'Consumidor'),
    (4, 'Admin'),
)

listaFormasDePago = (
        (1, 'Efectivo'),
        (2, 'Tarjeta de Débito'),
        (3, 'Tarjeta de Crédito'),
        (4, 'Tarjeta Junaeb'),
    )

listaCategorias = (
    (1, 'Snacks'),
    (2, 'Almuerzos'),
    )


class TipoUsuario(models.Model):
    tipo = models.CharField(max_length=100, choices=tiposUsuario)


class Avatars(models.Model):
    imagen = models.ImageField(upload_to='avatars')

    class Meta:
        db_table = 'avatars'


class Categorias(models.Model):
    categoria = models.CharField(max_length=100, choices=listaCategorias)

    class Meta:
        db_table = 'categorias'


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    avatar = models.ImageField(upload_to='avatars')
    tipo = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    def is_authenticated(self):
        return self.user.is_authenticated()

    def get_full_name(self):
        return self.nombre

    def get_short_name(self):
        return self.nombre

    def get_email(self):
        return self.email

    def get_user_type(self):
        return self.tipo.id

    def get_vendedor(self):
        return Vendedor.objects.get(usuario_ptr_id=self.id)

    def get_consumidor(self):
        return Consumidor.objects.get(usuario_ptr_id=self.id)

    def is_consumidor(self):
        return self.get_user_type() == 3

    def is_movil(self):
        return self.get_user_type() == 2

    def is_fijo(self):
        return self.get_user_type() == 1

    def is_vendedor(self):
        return self.is_movil() or self.is_fijo()

    def get_avatar(self):
        return self.avatar

    def efectivo(self):
        return self.get_vendedor().efectivo()

    def debito(self):
        return self.get_vendedor().debito()

    def credito(self):
        return self.get_vendedor().credito()

    def junaeb(self):
        return self.get_vendedor().junaeb()

    class Meta:
        db_table = 'usuario'


class Consumidor(Usuario):
    vendedoresFavoritos = MultiSelectField(blank=True, null=True)
    def __str__(self):
        return self.nombre + " " + super(self).tipo.tipo

    class Meta:
        db_table = 'consumidor'


class Vendedor(Usuario):
    formas_de_pago = MultiSelectField(choices=listaFormasDePago, null=True, blank=True)
    numfavoritos = models.IntegerField(default=0)
    lat = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    lng = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    def __str__(self):
        return self.user.__str__()

    def horas(self):
        f = '%H:%M %p'
        return '{} - {}'.format(self.fijo().horaIni.strftime(f), self.fijo().horaFin.strftime(f)) if self.is_fijo() else ''

    def is_active_now(self):
        return self.fijo().horaIni < datetime.now().time() < self.fijo().horaFin if self.is_fijo() else self.movil().activo

    def fijo(self):
        return VendedorFijo.objects.get(vendedor_ptr_id=self.id)

    def movil(self):
        return VendedorAmbulante.objects.get(vendedor_ptr_id=self.id)

    def efectivo(self):
        return "1" in self.formas_de_pago

    def debito(self):
        return "2" in self.formas_de_pago

    def credito(self):
        return "3" in self.formas_de_pago

    def junaeb(self):
        return "4" in self.formas_de_pago

    def formasDePago_toStr(self):
        res = ""
        if self.efectivo():
            res+="Efectivo "
        if self.debito():
            res+="Débito "
        if self.credito():
            res+="Crédito "
        if self.junaeb():
            res+="Junaeb"
        return res


    class Meta:
        db_table = 'vendedor'


class Favoritos(models.Model):
    consumidor = models.ForeignKey(Consumidor, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.today)

    def __str__(self):
        return self.consumidor.user.nombre + "->" + self.vendedor.nombre

    class Meta:
        db_table = 'favoritos'


class VendedorFijo(Vendedor):
    horaIni = models.TimeField(blank=True)
    horaFin = models.TimeField(blank=True)

    def __str__(self):
        return self.vendedor.__str__()

    class Meta:
        db_table = 'fijo'


class VendedorAmbulante(Vendedor):
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.vendedor.__str__()

    class Meta:
        db_table = 'ambulante'


class Admin(Usuario):

    def __str__(self):
        return self.nombre + " " + super(Usuario).tipo.tipo

    class Meta:
        db_table = 'admin'


class Producto(models.Model):
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    categorias = models.ForeignKey(Categorias)
    descripcion = models.CharField(max_length=400)
    stock = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    avatar = models.CharField(max_length=100, default='bread.png')
    imagen = models.ImageField(upload_to='productos')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'producto'


class Transacciones(models.Model):
    fecha = models.DateField(default=datetime.today)
    producto = models.ForeignKey(Producto)
    vendedor = models.ForeignKey(Vendedor)
    lat = models.DecimalField(max_digits=8, decimal_places=4, default=0, blank=True)
    lng = models.DecimalField(max_digits=8, decimal_places=4, default=0, blank=True)

    class Meta:
        db_table = 'transacciones'
