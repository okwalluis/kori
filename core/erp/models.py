from crum import get_current_user
from django.db import models
from datetime import datetime

from django.forms import model_to_dict
from core.control_stock.models import Producto, TipoOperacion, UnidadMedida
from core.base.models import Deposito, Empresa

from config.settings import MEDIA_URL, STATIC_URL
from core.erp.choices import gender_choices
from core.models import BaseModel
from core.dominios import TIPOS_CONCEPTOS, TIPOS_CAJAS

#concepto
#Moneda
#Caja 
#DetallesDebitoCredito
class Concepto(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa',null=True, blank=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    tipo = models.CharField(max_length=2, null=True, choices=TIPOS_CONCEPTOS,blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo'] = dict(TIPOS_CONCEPTOS).get(self.tipo, '') if self.tipo else ''
        return item

    class Meta:
        verbose_name = 'Conceptos'
        verbose_name_plural = 'Conceptos'
        db_table = 'conceptos'
        ordering = ['id']

class Moneda(BaseModel):
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    sigla = models.CharField(max_length=10, verbose_name='Sigla', unique=True)
    cantidad_decimales = models.IntegerField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['sigla'] = self.sigla
        item['cantidad_decimales'] = str(self.cantidad_decimales)
        return item

    class Meta:
        verbose_name = 'Monedas'
        verbose_name_plural = 'Monedas'
        db_table = 'monedas'
        ordering = ['id']

class Caja(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    descripcion = models.CharField(max_length=100, verbose_name='Descripción', unique=True)
    tipo = models.CharField(max_length=2, null=True, choices=TIPOS_CAJAS,blank=True)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.descripcion

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo'] = dict(TIPOS_CAJAS).get(self.tipo, '') if self.tipo else ''
        item['moneda'] = self.moneda.descripcion
        return item

    class Meta:
        verbose_name = 'Cajas'
        verbose_name_plural = 'Cajas'
        db_table = 'cajas'
        ordering = ['id']

class CabMovimiento(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    tipo_operacion = models.ForeignKey(TipoOperacion, on_delete=models.PROTECT, null=True, blank=True)
    numero = models.IntegerField()
    fecha = models.DateField(default=datetime.now)
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT, null=True, blank=True)
    observacion = models.CharField(max_length=150, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.numero

    def toJSON(self):
        item = model_to_dict(self)
        item['empresa'] = self.empresa.toJSON()
        item['tipo_operacion'] = self.tipo_operacion.toJSON()
        item['numero'] = self.numero
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['deposito'] = self.deposito.toJSON()
        item['observacion'] = self.observacion        
        item['detalle'] = [i.toJSON() for i in self.detmovimiento_set.all()]
        return item
 
    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        db_table = 'movimientos'
        ordering = ['id']
                
class DetalleDebitoCredito(BaseModel):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa', null=True, blank=True)
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha movimiento')
    concepto = models.ForeignKey(Concepto, on_delete=models.PROTECT)
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT)
    caja = models.ForeignKey(Caja, on_delete=models.PROTECT)
    valor_moneda = models.DecimalField(max_digits=16, decimal_places=4)
    valor_consolidado = models.DecimalField(max_digits=16, decimal_places=4)
    observacion = models.CharField(max_length=100, verbose_name='Observación', unique=True)
    
    def toJSON(self):
        item = model_to_dict(self.id)
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['concepto'] = self.concepto.toJSON()
        item['moneda'] = self.moneda.toJSON()
        item['valor_moneda'] = format(self.valor_moneda, '.4f')
        item['valor_consolidado'] = format(self.valor_moneda, '.4f')
        item['observacion'] = self.observacion        
        return item

    class Meta:
        verbose_name = 'Detalle débito/créditos'
        verbose_name_plural = 'Detalles débitos/créditos'
        db_table = 'detallesdebitocredito'
        ordering = ['id']

class DetMovimiento(models.Model):
    movimiento = models.ForeignKey(CabMovimiento, on_delete=models.CASCADE)
    item = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=12, decimal_places=4, default=0.0000)
    costo_mmnn = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    costo_docu = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.producto.toJSON()

    """
        def toJSON(self):
            return {
                'id': self.id,
                'descripcion': self.producto.descripcion,
                'categoria': self.producto.categoria.descripcion,
                'unidad_medida': self.unidad_medida.sigla,
                'cantidad': self.cantidad,
                'costo_mmnn': self.costo_mmnn
            } 
    """
    
    def toJSON(self):
        item = model_to_dict(self, exclude=['movimiento'])
        item['item']= self.item
        item['producto'] = self.producto.toJSON()
        item['unidad_medida'] = self.unidad_medida.toJSON()
        item['cantidad'] = format(self.cantidad, '.2f')
        item['costo_mmnn'] = format(self.costo_mmnn, '.2f')
        item['costo_docu'] = format(self.costo_docu, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Movimiento'
        verbose_name_plural = 'Detalles de Movimiento'
        db_table = 'movimientos_det'
        ordering = ['movimiento']

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2, verbose_name='Precio de venta')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        item['cat'] = self.cat.toJSON()
        item['image'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    date_birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Dirección')
    gender = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['date_birthday'] = self.date_birthday.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['id']

class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

    def toJSON(self):
        item = model_to_dict(self)
        item['cli'] = self.cli.toJSON()
        item['subtotal'] = format(self.subtotal, '.2f')
        item['iva'] = format(self.iva, '.2f')
        item['total'] = format(self.total, '.2f')
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['det'] = [i.toJSON() for i in self.detsale_set.all()]
        return item

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['id']

class DetSale(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['prod'] = self.prod.toJSON()
        item['price'] = format(self.price, '.2f')
        item['subtotal'] = format(self.subtotal, '.2f')
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        ordering = ['id']

