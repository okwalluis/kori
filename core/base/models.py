from django.db import models
from django.forms import model_to_dict

from core.dominios import TIPOS_PERSONA, GENEROS, ESTADOS_CIVILES
from core.models import BaseModel

class Persona(BaseModel):
    nombre = models.CharField(max_length=200, null=True, blank=True) 
    apellido = models.CharField(max_length=100, null=True, blank=True)
    razon_social = models.CharField(max_length=200)
    nombre_fantasia = models.CharField(max_length=200, null=True, blank=True)
    tipo_persona = models.CharField(max_length=1, null=True, choices=TIPOS_PERSONA,blank=True)
    fecha_nacimiento = models.DateField(null=True)
    genero = models.CharField(max_length=1, null=True, choices=GENEROS,blank=True)
    estado_civil = models.CharField(max_length=2, null=True, choices=ESTADOS_CIVILES,blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.nombre
        item['apellido'] = self.apellido
        item['nombre_fantasia'] = self.nombre_fantasia
        item['tipo_persona'] = dict(TIPOS_PERSONA)[self.tipo_persona] if self.tipo_persona else ''
        item['genero'] = dict(GENEROS)[self.genero] if self.genero else ''
        item['estado_civil'] = dict(ESTADOS_CIVILES).get(self.estado_civil, '') if self.estado_civil else ''
        return item

#    def get_image(self):
#        if self.image:
#            return '{}{}'.format(MEDIA_URL, self.image)
#        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        db_table = 'personas'
        verbose_name_plural = 'Personas'
        db_table = 'personas'
        ordering = ['id']

class Pais(BaseModel):
    descripcion = models.CharField(max_length=80)
    sigla   = models.CharField(max_length=5, unique=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['sigla'] = self.sigla
        return item

    class Meta:
        db_table = 'País'
        verbose_name_plural = 'Países'
        db_table = 'paises'
        ordering = ['id']
    
class Empresa(BaseModel):
    descripcion = models.CharField(max_length=80)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, null=True, blank=True)
    ruc = models.CharField(max_length=20, unique=True, null=True, blank=True)
    representante = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True, related_name='representante')
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, null=True, blank=True, related_name='persona')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion
    
    def toJSON(self):
        item = model_to_dict(self)
        item['pais'] = self.pais.descripcion  if self.pais else ''
        item['ruc'] = self.ruc
        item['representante'] = self.representante.razon_social  if self.representante else ''
        item['persona'] = self.persona.razon_social  if self.persona else ''
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'empresas'
        ordering = ['id']
        
class Sucursal(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=80)
    direccion = models.CharField(max_length=100, unique=True, null=True, blank=True)
    localidad = models.CharField(max_length=50, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=50, unique=True, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion
    
    def toJSON(self):
        item = model_to_dict(self)
        item['empresa'] = self.empresa.descripcion  if self.empresa else ''
        item['descripcion'] = self.descripcion
        item['direccion'] = self.direccion if self.direccion else ''
        item['localidad'] = self.localidad if self.localidad else ''
        item['telefono'] = self.telefono if self.telefono else ''
        
        return item

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        db_table = 'sucursales'
        ordering = ['id']

class Deposito(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=80)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion
    
    def toJSON(self):
        item = model_to_dict(self)
        item['empresa'] = self.empresa.descripcion  if self.empresa else ''
        item['descripcion'] = self.descripcion
        item['sucursal'] = self.sucursal.descripcion  if self.sucursal else ''
        return item

    class Meta:
        verbose_name = 'Deposito'
        verbose_name_plural = 'Depositos'
        db_table = 'depositos'
        ordering = ['id']