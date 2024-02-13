import datetime
from enum import Enum
from django.db import models
from django.forms import model_to_dict
from core.base.models import Deposito, Empresa

from config.settings import MEDIA_URL, STATIC_URL
from core.dominios import TIPOS_PRODUCTOS, PRODUCTOS_BIENES, TIPOS_OPER_STOCK, TIPO_OPERADOR_ARIT
from core.models import BaseModel

class Categoria(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'
        ordering = ['id']

class SubCategoria(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        return item

    class Meta:
        verbose_name = 'Sub-Categoria'
        verbose_name_plural = 'Sub-Categorias'
        db_table = 'subcategoria'
        ordering = ['id']

class UnidadMedida(BaseModel):
    descripcion = models.CharField(max_length=80, verbose_name='Descripción', unique=True)
    sigla = models.CharField(max_length=10, verbose_name='Sigla', unique=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['sigla'] = self.sigla
        return item

    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medidas'
        db_table = 'unidadesmedidas'
        ordering = ['id']

class Producto(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, verbose_name='SubCategoría')
    tipo = models.CharField(max_length=2, null=True, choices=TIPOS_PRODUCTOS,blank=True)
    subtipo = models.CharField(max_length=2, null=True, choices=PRODUCTOS_BIENES,blank=True)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE, verbose_name='Unidad medida')
    codigo_barra = models.CharField(max_length=30, verbose_name='Cód. Barra', unique=True, blank=True, null=True)
    codigo_fabrica = models.CharField(max_length=30, verbose_name='Cód. Fábrica', unique=True, blank=True, null=True)
    imagen = models.ImageField(upload_to='producto/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    controla_lote = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    #existencia minima
    #historico de impuesto
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['descripcion'] = self.descripcion if self.descripcion else ''
        item['categoria'] = self.categoria.descripcion if self.categoria else ''
        item['subcategoria'] = self.subcategoria.descripcion if self.subcategoria else ''
        item['tipo'] = dict(TIPOS_PRODUCTOS).get(self.tipo, '') if self.tipo else ''
        item['subtipo'] = dict(PRODUCTOS_BIENES).get(self.subtipo, '') if self.subtipo else ''
        item['unidad_medida'] = self.unidad_medida.toJSON() if self.unidad_medida else ''
        item['codigo_barra'] = self.codigo_barra if self.codigo_barra else ''
        item['codigo_fabrica'] = self.codigo_fabrica if self.codigo_fabrica else ''
        item['imagen'] = self.get_image()
        return item

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(MEDIA_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'productos'
        ordering = ['id']

class Lote(BaseModel):
    producto = models.ForeignKey(Producto, on_delete= models.PROTECT)
    numero_lote = models.CharField(max_length=50, verbose_name='Descripción', default='0000')
    fecha_elaboracion = models.DateField(verbose_name='Fecha elaboración')
    fecha_vencimiento = models.DateField(verbose_name='Fecha vencimiento', null=True, blank=True)

    def __str__(self):
        return f'{self.numero_lote}'

    def toJSON(self):
        item = model_to_dict(self)
        item['producto'] = self.producto.descripcion
        item['fecha_elaboracion'] = self.fecha_elaboracion.strftime('%Y-%m-%d')
        item['fecha_vencimiento'] = self.fecha_vencimiento.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Lote'
        verbose_name_plural = 'Lotes'
        db_table = 'lotes'
        ordering = ['id']

class TipoOperacion(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    sigla = models.CharField(max_length=20, verbose_name='Sigla', unique=True)
    tipo = models.CharField(max_length=2, null=True, choices=TIPOS_OPER_STOCK,blank=True)
    afecta_costo = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['empresa'] = self.empresa.toJSON()
        item['descripcion'] = self.descripcion 
        item['sigla'] = self.sigla
        item['tipo'] = dict(TIPOS_OPER_STOCK).get(self.tipo, '') if self.tipo else ''
        item['afecta_costo'] = 'Si' if self.tipo else 'No'
        return item

    class Meta:
        verbose_name = 'Tipo Operacion'
        verbose_name_plural = 'Tipos operaciones'
        db_table = 'tipos_operaciones_stock'
        ordering = ['id']

class Operador(Enum):
    MULTIPLICA = 'Multiplica'
    DIVIDE = 'Divide'
    POTENCIA = 'Potencia'

class ConversionMedida(BaseModel):
    medida_de = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name='medida_de')
    medida_a = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT, related_name='medida_a')
    operacion = models.CharField(max_length=2, null=True, choices=TIPO_OPERADOR_ARIT,blank=True)
    valor = models.FloatField(default=0.0000)
    activo = models.BooleanField(default=True)


    def __str__(self):
        return self.medida_de.sigla + 'a ' + self.medida_a.sigla

    def toJSON(self):
        item = model_to_dict(self)
        item['medida_de'] = self.medida_de.descripcion if self.medida_de else ''
        item['medida_a'] = self.medida_a.descripcion if self.medida_a else ''
        item['operacion'] = dict(TIPO_OPERADOR_ARIT).get(self.operacion, '') if self.operacion else ''
        item['valor'] = self.valor
        return item
    
    class Meta:
        db_table = 'conversiones_medidas'
        verbose_name = 'Conversion de medida'
        verbose_name_plural = 'Conversiones de Medidas'
        ordering = ['id']
        
class MovimientoProductoFecha(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete= models.PROTECT)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete= models.PROTECT)
    fecha = models.DateField()
    saldo_anterior = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)
    entrada = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)
    salida = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)
    saldo = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)

    def __str__(self):
        return '[' + self.deposito.descripcion + '] [' + self.producto.descripcion + ']' + self.saldo

    def toJSON(self):
        item = model_to_dict(self)
        item['deposito'] = self.deposito.toJSON()
        item['producto'] = self.producto.toJSON()
        item['unidad_medida'] = self.unidad_medida.toJSON()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['saldo_anterior'] = format(self.saldo_anterior, '.4f')
        item['entrada'] = format(self.entrada, '.4f')
        item['salida'] = format(self.salida, '.4f')
        item['saldo'] = format(self.saldo, '.4f')
        return item
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deposito', 'producto', 'fecha'], name='movimientos_productos_fecha_pk'),
        ]
        db_table = 'movimientos_productos_fecha'
        verbose_name = 'Movimiento de producto por fecha'
        verbose_name_plural = 'Movimientos de productos por fecha'
        ordering = ['id']
    

class ExistenciaProducto(models.Model):
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    saldo = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)

    def __str__(self):
        return f'[{self.deposito}] [{self.producto.descripcion}] = {self.saldo}'

    def toJSON(self):
        item = model_to_dict(self)
        item['deposito'] = self.deposito.toJSON()
        item['producto'] = self.producto.toJSON()
        item['saldo'] = format(self.saldo, '.4f')        
        return item

    class Meta:
        # Define los campos deposito y producto como clave primaria
        constraints = [
            models.UniqueConstraint(fields=['deposito', 'producto'], name='existencia_producto_pk'),
        ]
        db_table = 'existencias_productos'
        verbose_name = 'Existencia de producto'
        verbose_name_plural = 'Existencias de productos'
        ordering = ['id']