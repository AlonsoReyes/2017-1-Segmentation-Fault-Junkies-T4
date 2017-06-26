# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatars',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('imagen', models.ImageField(upload_to='avatars')),
            ],
            options={
                'db_table': 'avatars',
            },
        ),
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('categoria', models.CharField(choices=[(1, 'Snacks'), (2, 'Almuerzos')], max_length=100)),
            ],
            options={
                'db_table': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('fecha', models.DateField(default=datetime.datetime.today)),
            ],
            options={
                'db_table': 'favoritos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('tipo', models.CharField(choices=[(1, 'Fijo'), (2, 'Ambulante'), (3, 'Consumidor'), (4, 'Admin')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transacciones',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('fecha', models.DateField(default=datetime.datetime.today)),
                ('lat', models.DecimalField(blank=True, max_digits=8, decimal_places=4, default=0)),
                ('lng', models.DecimalField(blank=True, max_digits=8, decimal_places=4, default=0)),
                ('producto', models.ForeignKey(to='main.Producto')),
            ],
            options={
                'db_table': 'transacciones',
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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
                ('usuario_ptr', models.OneToOneField(parent_link=True, to='main.Usuario', serialize=False, primary_key=True, auto_created=True)),
            ],
            options={
                'db_table': 'admin',
            },
            bases=('main.usuario',),
        ),
        migrations.CreateModel(
            name='Consumidor',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, to='main.Usuario', serialize=False, primary_key=True, auto_created=True)),
                ('vendedoresFavoritos', multiselectfield.db.fields.MultiSelectField(max_length=200, blank=True, null=True)),
            ],
            options={
                'db_table': 'consumidor',
            },
            bases=('main.usuario',),
        ),
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('usuario_ptr', models.OneToOneField(parent_link=True, to='main.Usuario', serialize=False, primary_key=True, auto_created=True)),
                ('formas_de_pago', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Efectivo'), (2, 'Tarjeta de Débito'), (3, 'Tarjeta de Crédito'), (4, 'Tarjeta Junaeb')], max_length=7, blank=True, null=True)),
                ('numfavoritos', models.IntegerField(default=0)),
                ('lat', models.DecimalField(max_digits=8, decimal_places=4, default=0)),
                ('lng', models.DecimalField(max_digits=8, decimal_places=4, default=0)),
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
                ('vendedor_ptr', models.OneToOneField(parent_link=True, to='main.Vendedor', serialize=False, primary_key=True, auto_created=True)),
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
                ('vendedor_ptr', models.OneToOneField(parent_link=True, to='main.Vendedor', serialize=False, primary_key=True, auto_created=True)),
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
