from django.db import models
from django.forms import model_to_dict

from core.models import BaseModel

class Impuesto(BaseModel):
    descripcion = models.CharField(max_length=50)
    porcentaje = models.FloatField()
    base_imponible = models.FloatField()
    impuesto_incluido = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['porcentaje'] = format(self.porcentaje, '.2f')
        item['base_imponible'] = format(self.base_imponible, '.2f')
        return item

    class Meta:
        verbose_name = 'Impuesto'
        verbose_name_plural = 'Impuestos'
        db_table = 'impuestos'
        ordering = ['id']