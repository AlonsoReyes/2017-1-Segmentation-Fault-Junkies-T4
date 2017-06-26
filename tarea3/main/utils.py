from .models import *
from django.utils.timezone import datetime


def nuevoUser(form):
    user = User.objects.create_user(username=form['email'], email=form['email'], password=form['password'])
    user.save()
    return user


def nuevoUsuario(form):
    nuevoUser(form)
    user = User.objects.get(username=form['email'])
    tiposUsuario = TipoUsuario.objects.get(id=int(form['tipo']))
    if form['avatar'] == '':
        usuario = Usuario(user=user, tipo=tiposUsuario, nombre=form['nombre'], email=form['email'])
    else:
        usuario = Usuario(user=user, avatar=form['avatar'], tipo=tiposUsuario, nombre=form['nombre'], email=form['email'])
    usuario.save()
    return usuario


def nuevoConsumidor(form):
    nuevoUser(form)
    user = User.objects.get(username=form['email'])
    tiposUsuario = TipoUsuario.objects.get(id=int(form['tipo']))
    consumidor = Consumidor(user=user, tipo=tiposUsuario, nombre=form['nombre'], email=form['email'], avatar=form['avatar'])
    consumidor.save()
    return consumidor


def nuevoVendedorFijo(form, pagos):
    nuevoUser(form)
    tiposUsuario = TipoUsuario.objects.get(id=int(form['tipo']))
    user = User.objects.get(username=form['email'])
    vendedor = VendedorFijo(user=user, tipo=tiposUsuario, nombre=form['nombre'], email=form['email'], avatar=form['avatar'],
                            horaIni=form['horaIni'], horaFin=form['horaFin'])
    vendedor.save()
    vendedor.formas_de_pago = pagos
    vendedor.save()
    return vendedor


def nuevoVendedorAmbulante(form, pagos):
    nuevoUser(form)
    tiposUsuario = TipoUsuario.objects.get(id=int(form['tipo']))
    user = User.objects.get(username=form['email'])
    vendedor = VendedorAmbulante(user=user, tipo=tiposUsuario, nombre=form['nombre'], email=form['email'],
                            avatar=form['avatar'])
    vendedor.save()
    vendedor.formas_de_pago = pagos
    vendedor.save()
    return vendedor


def agregarProducto(form, vendedor):
    producto = Producto(vendedor=vendedor, nombre=form['nombre'], precio=int(form['precio']), stock=int(form['stock']),
                        descripcion=form['descripcion'], avatar=form['avatar'], imagen=form['imagen'],
                        categorias=Categorias.objects.get(id=int(form['categorias'])))
    producto.save()


def editarProducto(form, producto, avatar):
    producto.nombre=form['nombre']
    producto.descripcion=form['descripcion']
    producto.precio=form['precio']
    producto.stock=form['stock']
    producto.avatar=form['avatar']
    producto.categorias = Categorias.objects.get(id=int(form['categorias']))
    producto.avatar = avatar
    if form['imagen'] is not None:
        producto.imagen = form['imagen']
    producto.save()


def crearTransaccion(vendedor, producto):
    t = Transacciones(producto=producto, vendedor=vendedor, fecha=datetime.today(), lat=vendedor.lat, lng=vendedor.lng)
    t.save()
    print("call")


def getPagos(req):
    pagos = []
    if req.get('efectivo') is not None:
        pagos.append("1")
    if req.get('credito') is not None:
        pagos.append("2")
    if req.get('debito') is not None:
        pagos.append("3")
    if req.get('junaeb') is not None:
        pagos.append("4")
    return pagos


def editarCuenta(usuario, pagos, form):
    if usuario.tipo.id in [1, 2]:
        vendedor = usuario.get_vendedor()
        usuario.nombre = form['nombre']
        if form['avatar'] is not None:
            usuario.avatar = form['avatar']
        usuario.save()
        vendedor.nombre = form['nombre']
        if form['avatar'] is not None:
            vendedor.avatar = form['avatar']
        vendedor.formas_de_pago = pagos
        vendedor.save()
        if usuario.tipo.id == 1:
            fijo = vendedor.fijo()
            fijo.horaIni = form['horaIni']
            fijo.horaFin = form['horaFin']
            fijo.save()
    if usuario.tipo.id == 3:
        consumidor = usuario.get_consumidor()
        usuario.nombre = form['nombre']
        if form['avatar'] is not None:
            usuario.avatar = form['avatar']
        usuario.save()
        consumidor.nombre = form['nombre']
        if form['avatar'] is not None:
            consumidor.avatar = form['avatar']
        consumidor.save()
