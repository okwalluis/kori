# Generated by Django 4.2.6 on 2024-01-20 20:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('descripcion', models.CharField(max_length=80)),
                ('direccion', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('localidad', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('telefono', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('activo', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.empresa')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sucursal',
                'verbose_name_plural': 'Sucursales',
                'db_table': 'sucursales',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Deposito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('descripcion', models.CharField(max_length=80)),
                ('activo', models.BooleanField(default=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.empresa')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.sucursal')),
            ],
            options={
                'verbose_name': 'Deposito',
                'verbose_name_plural': 'Depositos',
                'db_table': 'depositos',
                'ordering': ['id'],
            },
        ),
    ]
