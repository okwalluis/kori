# Generated by Django 4.2.6 on 2024-01-27 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control_stock', '0004_tipooperacion_conversionmedida'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversionmedida',
            name='operacion',
            field=models.CharField(blank=True, choices=[('M', 'Multiplica'), ('D', 'Divide')], max_length=2, null=True),
        ),
    ]
