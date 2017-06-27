# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatars',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('imagen', models.ImageField(upload_to='avatars')),
            ],
            options={
                'db_table': 'avatars',
            },
        ),
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('categoria', models.CharField(max_length=100, choices=[(1, 'Snacks'), (2, 'Almuerzos')])),
            ],
            options={
                'db_table': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField(default=datetime.datetime.today)),
            ],
            options={
                'db_table': 'favoritos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.CharField(max_length=400)),
                ('stock', models.IntegerField(default=0)),
                ('precio', models.IntegerField(default=0)),
                ('avatar', models.CharField(max_length=100, default='bread.png')),
                ('imagen', models.ImageField(upload_to='productos')),
                ('categorias', models.ForeignKey(to='main.Categorias')),
            ],
            options={
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('tipo', models.CharField(max_length=100, choices=[(1, 'Fijo'), (2, 'Ambulante'), (3, 'Consumidor'), (4, 'Admin')])),
            ],
        ),
        migrations.CreateModel(
            name='Transacciones',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('fecha', models.DateField(default=datetime.datetime.today)),
                ('lat', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=8)),
                ('lng', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=8)),
                ('producto', models.ForeignKey(to='main.Producto')),
            ],
            options={
                'db_table': 'transacciones',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('avatar', models.ImageField(upload_to='avatars')),
            ],
            options={
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, to='main.Usuario', primary_key=True, serialize=False, parent_link=True)),
            ],
            options={
                'db_table': 'admin',
            },
            bases=('main.usuario',),
        ),
        migrations.CreateModel(
            name='Consumidor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, to='main.Usuario', primary_key=True, serialize=False, parent_link=True)),
                ('vendedoresFavoritos', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=200, null=True)),
            ],
            options={
                'db_table': 'consumidor',
            },
            bases=('main.usuario',),
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('usuario_ptr', models.OneToOneField(auto_created=True, to='main.Usuario', primary_key=True, serialize=False, parent_link=True)),
                ('formas_de_pago', multiselectfield.db.fields.MultiSelectField(blank=True, max_length=7, null=True, choices=[(1, 'Efectivo'), (2, 'Tarjeta de Débito'), (3, 'Tarjeta de Crédito'), (4, 'Tarjeta Junaeb')])),
                ('numfavoritos', models.IntegerField(default=0)),
                ('lat', models.DecimalField(decimal_places=4, default=0, max_digits=8)),
                ('lng', models.DecimalField(decimal_places=4, default=0, max_digits=8)),
            ],
            options={
                'db_table': 'vendedor',
            },
            bases=('main.usuario',),
        ),
        migrations.AddField(
            model_name='usuario',
            name='tipo',
            field=models.ForeignKey(to='main.TipoUsuario'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='VendedorAmbulante',
            fields=[
                ('vendedor_ptr', models.OneToOneField(auto_created=True, to='main.Vendedor', primary_key=True, serialize=False, parent_link=True)),
                ('activo', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ambulante',
            },
            bases=('main.vendedor',),
        ),
        migrations.CreateModel(
            name='VendedorFijo',
            fields=[
                ('vendedor_ptr', models.OneToOneField(auto_created=True, to='main.Vendedor', primary_key=True, serialize=False, parent_link=True)),
                ('horaIni', models.TimeField(blank=True)),
                ('horaFin', models.TimeField(blank=True)),
            ],
            options={
                'db_table': 'fijo',
            },
            bases=('main.vendedor',),
        ),
        migrations.AddField(
            model_name='transacciones',
            name='vendedor',
            field=models.ForeignKey(to='main.Vendedor'),
        ),
        migrations.AddField(
            model_name='producto',
            name='vendedor',
            field=models.ForeignKey(to='main.Vendedor'),
        ),
        migrations.AddField(
            model_name='favoritos',
            name='consumidor',
            field=models.ForeignKey(to='main.Consumidor'),
        ),
        migrations.AddField(
            model_name='favoritos',
            name='vendedor',
            field=models.ForeignKey(to='main.Vendedor'),
        ),
    ]
