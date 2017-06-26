from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^auth/$', views.auth_view, name='autenticacion'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit_auth/$', views.edit_auth, name='edit_auth'),
    url(r'^activeChange/$', views.ajaxActive, name = 'ajaxActive'),
    url(r'^gestion_productos/$', views.gestion_productos, name = 'gestion_productos'),
    url(r'^addItem_auth/$', views.addItem_auth, name='addItem_auth'),
    url(r'^edit_prod/(?P<producto_id>\d+)/$', views.edit_prod, name='edit_prod'),
    url(r'^edit_prod_auth/$', views.edit_prod_auth, name='edit_prod_auth'),
    url(r'^elim_prod/$', views.elim_prod, name='elim_prod'),
    url(r'^downStockTransaction/$', views.ajaxDownTransaction, name='ajaxDownTransaction'),
    url(r'^upStock/$', views.ajaxUpStock, name='ajaxUpStock'),
    url(r'^favChange/$', views.ajaxFavChange, name='ajaxFavChange'),
    url(r'^(?P<vendedor_id>\d+)/$', views.vendedor_perfil, name='vendedor_perfil'),
    url(r'^estadisticas/$', views.estadisticas, name='estadisticas'),
    url(r'^editGraf/$', views.ajaxEditGraf, name='ajaxEditGraf'),
]

""""
    
    
    
    
    
    
    """