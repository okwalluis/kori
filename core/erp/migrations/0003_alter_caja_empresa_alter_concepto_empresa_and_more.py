# Generated by Django 4.2.6 on 2024-01-11 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_initial'),
        ('erp', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caja',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.empresa', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='concepto',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.empresa', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='detalledebitocredito',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.empresa', verbose_name='Empresa'),
        ),
    ]
