from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.http import JsonResponse
from .utils import *
from django.utils.timezone import datetime, timedelta
from django.db.models import Count, Sum
import json as simplejson

formasDePagoLista = (
        (1, 'Efectivo'),
        (2, 'Tarjeta de Crédito'),
        (3, 'Tarjeta de Débito'),
        (4, 'Tarjeta Junaeb'),
    )


def index(request):
    activo = False
    user = request.user
    if user.is_anonymous():
        return render_to_response('main/index.html', {'user': user, 'activo': activo})
    usuario = Usuario.objects.get(user_id=user.id)
    if usuario.tipo.id in [1, 2]:
        v = usuario.get_vendedor()
        try:
             p = Producto.objects.filter(vendedor_id=v.id)
        except:
            p = []

        if usuario.tipo.id == 2:
            return render_to_response('main/vendedor_perfil.html', {'userB': user, 'user': usuario, 'vendedor': v, 'activo' : usuario.get_vendedor().is_active_now(), 'productos' : p})
        if usuario.tipo.id == 1:
            return render_to_response('main/vendedor_perfil.html', {'userB': user, 'user': usuario, 'vendedor': v, 'activo': usuario.get_vendedor().is_active_now(), 'productos' : p})
    else:
        return render_to_response('main/index.html', {'userB': user, 'user': usuario, 'activo': activo})


def signup(request):
    form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


def login(request):
    c = {}
    c.update(csrf(request))
    form = LoginForm()
    c['form'] = form
    return render_to_response('main/login.html', c)


def logout(request):
    auth.logout(request)
    return redirect('/main/')


def auth_view(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=email, password=password)

    if user is not None:
        auth.login(request, user)
        print(request.user.is_authenticated())
        return HttpResponseRedirect('/main/')
    else:
        return HttpResponseRedirect('/main/login/')


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password2']:
                return render(request, 'main/singup.html', {'form': form})

            tipoUsuario = form.cleaned_data['tipo']
            pagos = getPagos(request.POST)
            if tipoUsuario == "3":
                nuevoConsumidor(form.cleaned_data)
            if tipoUsuario == "2":
                nuevoVendedorAmbulante(form.cleaned_data, pagos)
            if tipoUsuario == "1":
                nuevoVendedorFijo(form.cleaned_data, pagos)
            return HttpResponseRedirect('/main/login')
        else:
            form = SignUpForm()
            return render(request, 'main/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'main/signup.html', {'form': form})


@login_required
def edit(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    activo = False
    avatar = usuario.avatar
    initial = {'nombre': usuario.nombre, 'avatar': avatar, 'email': usuario.email}
    if usuario.tipo.id in [1, 2]:
        vendedor = usuario.get_vendedor()
        activo = vendedor.is_active_now()
        if vendedor.is_fijo():
            initial['horaIni'] = vendedor.fijo().horaIni
            initial['horaFin'] = vendedor.fijo().horaFin

    form = SignUpBaseForm(initial=initial)
    return render(request, 'main/edit.html', {'form': form, 'user': usuario,
                                                   'activo': activo,
                                                   'userB': user})


@login_required
def edit_auth(request):
    if request.method == 'POST':
        form = SignUpBaseForm(request.POST, request.FILES)
        user = request.user
        usuario = Usuario.objects.get(user=user)
        if form.is_valid():
            editarCuenta(usuario, getPagos(request.POST), form.cleaned_data)
            return HttpResponseRedirect('/main/')
        return HttpResponseRedirect('/main/')
    return HttpResponseRedirect('/main/')


@login_required
def gestion_productos(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    form = ItemForm()
    categorias = Categorias.objects.all()
    return render(request, 'main/gestion_productos.html', {'categorias': categorias, 'form': form, 'user': usuario,
                                                                'userB': user})


@login_required
def addItem_auth(request):
    if request.method == 'POST':
        user = request.user
        usuario = Usuario.objects.get(user=user)
        form = ItemForm(request.POST, request.FILES)
        vendedor = usuario.get_vendedor()
        if form.is_valid():
            agregarProducto(form.cleaned_data, vendedor)
        return redirect ('/main/')
    else:
        return redirect ('/main/gestion_productos')


@login_required
def edit_prod(request, producto_id=1):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    vendedor = usuario.get_vendedor()
    p = Producto.objects.get(id=producto_id)
    initial = {'nombre': p.nombre, 'descripcion': p.descripcion, 'precio': p.precio, 'stock': p.stock, 'avatar': p.avatar,
               'imagen': p.imagen, 'categorias': p.categorias.id}
    form = ItemForm(initial=initial)
    categorias = Categorias.objects.all()
    return render(request, 'main/edit_prod.html', {'categorias' : categorias, 'item': p, 'idprod': producto_id,
                                                        'form': form, 'user': usuario,
                                                        'activo': vendedor.is_active_now(),
                                                        'userB': user})


@login_required
def edit_prod_auth(request):
    if request.method == 'POST':
        user = request.user
        usuario = Usuario.objects.get(user=user)
        prod_id = request.POST.get('producto_id')
        prod_id = int(prod_id)
        producto = Producto.objects.get(id=prod_id)
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = request.POST.get('avatar')
            imagen = request.POST.get('imagen')
            editarProducto(form.cleaned_data, producto, avatar)
            return redirect('/main/')
        else:
            return redirect ('/main/edit_prod'+'/'+str(prod_id)+'/')
    else:
        return redirect ('/main/')


@login_required
def elim_prod(request):
    if request.method == 'POST':
        id = request.POST.get('producto_id')
        producto = Producto.objects.filter(id=id)
        producto.delete()
        return redirect('/main/')
    else:
        return redirect('/main/')


def vendedor_perfil(request, vendedor_id = 1):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    c = usuario.get_consumidor()
    activo = False
    try:
        v = Vendedor.objects.get(id=vendedor_id)
    except:
        return redirect('/main/')

    try:
        p = Producto.objects.filter(vendedor_id=v.id)
    except:
        p = []

    activo = v.is_active_now()
    fav = Favoritos.objects.filter(consumidor=c, vendedor=v).values()
    if not fav:
        favorito = False
    else:
        favorito = True
    return render_to_response('main/vendedor_perfil.html', {'userB': user, 'user': usuario,
                                                                 'activo': activo, 'vendedor' : v, 'productos' : p,
                                                                 'favorito': favorito})


def ajaxActive(request):
    act = request.GET.get('activo', None)
    user = request.user
    usuario = Usuario.objects.get(user=user)
    v = usuario.get_vendedor()
    m = v.movil()
    acti = None
    if act == 'true':
        acti = True
    if act == 'false':
        acti = False
    m.activo = acti
    m.save()
    return



def ajaxDownTransaction(request):
    prod_id = int(request.GET.get('producto_id', None))
    user = request.user
    usuario = Usuario.objects.get(user=user)
    vendedor = usuario.get_vendedor()
    producto = Producto.objects.get(id=prod_id)
    crearTransaccion(vendedor, producto)
    producto.stock -= 1
    producto.save()
    return JsonResponse({'stock': producto.stock})


def ajaxUpStock(request):
    prod_id = int(request.GET.get('producto_id', None))
    user = request.user
    producto = Producto.objects.get(id=prod_id)
    producto.stock += 1
    producto.save()
    return JsonResponse({'stock': producto.stock})


def ajaxFavChange(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    consumidor = usuario.get_consumidor()
    v_id = int(request.GET.get('v_id', None))
    vendedor = Vendedor.objects.get(id=v_id)
    favItem = Favoritos.objects.filter(consumidor=consumidor, vendedor=vendedor).values()
    if not favItem:
        fav = Favoritos(consumidor=consumidor, vendedor=vendedor, fecha=datetime.today())
        fav.save()
        consumidor.vendedoresFavoritos.append(str(v_id))
        consumidor.save()
        vendedor.numfavoritos += 1
        vendedor.save()
    else:
        fav = Favoritos.objects.filter(consumidor=consumidor, vendedor=vendedor)
        fav.delete()
        consumidor.vendedoresFavoritos.remove(str(v_id))
        vendedor.numfavoritos -= 1
        vendedor.save()


def estadisticas(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    vendedor = usuario.get_vendedor()
    trvend = Transacciones.objects.filter(vendedor=vendedor)
    trvend = trvend.filter(fecha__lte=datetime.today(), fecha__gte=datetime.today() - timedelta(days=4)).values('producto').annotate(conteo=Count('producto'))
    listaTransac = list(trvend)
    productos = []
    cantidad = []
    aux = []
    for i in listaTransac:
        #aux.append(Producto.objects.get(id=int(i['producto'])).nombre)
        #aux.append(int(i['conteo']))
        productos.append(Producto.objects.get(id=int(i['producto'])).nombre)
        cantidad.append(int(i['conteo']))

    #productosCantidadArr = simplejson.dumps(productosCantidad)
    favoritQS = Favoritos.objects.filter(vendedor=vendedor, fecha__lte=datetime.today(), fecha__gte=datetime.today() - timedelta(days=4)).values('vendedor').annotate(conteo=Count('vendedor'))
    listaFav = list(favoritQS)
    favoritos = []
    for i in listaFav:
        favoritos.append(int(i['conteo']))
    return render(request, 'main/estadisticas.html', {'userB': user, 'user': usuario, 'vendedor': vendedor,
                                                           'activo': usuario.get_vendedor().is_active_now(),
                                                           'productosGraficar': simplejson.dumps(productos),
                                                           'cantidadGraficar': simplejson.dumps(cantidad),
                                                           'numFav': simplejson.dumps(favoritos)})


#Entrega bien los resultados, falta hacer cambios en html "estadisticas".
def ajaxEditGraf(request):
    user = request.user
    usuario = Usuario.objects.get(user=user)
    vendedor = usuario.get_vendedor()
    iniDate = request.GET.get('ini', None)
    print(iniDate)
    iniDate = iniDate.replace("/", "-")
    finDate = request.GET.get('fin', None)
    finDate = finDate.replace("/", "-")

    if iniDate == "" and finDate == "":
        finDate = datetime.today()
        iniDate = finDate - timedelta(days=4)
    if iniDate == "" and finDate != "":
        finDate = datetime.strptime(finDate, '%Y-%m-%d')
        iniDate = finDate - timedelta(days=4)
    if iniDate != "" and finDate == "":
        finDate = datetime.today()
        iniDate = datetime.strptime(iniDate, '%Y-%m-%d')
    else:
        iniDate = datetime.strptime(iniDate, '%Y-%m-%d')
        finDate = datetime.strptime(finDate, '%Y-%m-%d')
    print("alo")
    if iniDate.date() > finDate.date():
        return redirect('/main/estadisticas/')
    trvend = Transacciones.objects.filter(vendedor=vendedor)

    trvend = trvend.filter(fecha__lte=finDate, fecha__gte=iniDate).values(
        'producto').annotate(conteo=Count('producto'))

    listaTransac = list(trvend)
    productos = []
    cantidad = []
    for i in listaTransac:
        productos.append(Producto.objects.get(id=int(i['producto'])).nombre)
        cantidad.append(int(i['conteo']))

    favoritQS = Favoritos.objects.filter(vendedor=vendedor, fecha__lte=finDate,
                                         fecha__gte=iniDate).values('vendedor').annotate(
        conteo=Count('vendedor'))

    listaFav = list(favoritQS)
    favoritos = []
    for i in listaFav:
        favoritos.append(int(i['conteo']))
    print(productos)
    print(cantidad)
    print(favoritos)
    return JsonResponse({'productosGraficar': simplejson.dumps(productos),
                         'cantidadGraficar': simplejson.dumps(cantidad),
                         'numFav': simplejson.dumps(favoritos)})


