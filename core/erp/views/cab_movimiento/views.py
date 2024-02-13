from decimal import Decimal
from django.db import transaction
from django.db.models import Max

import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin

from core.control_stock.models import (
    MovimientoProductoFecha,
    Producto,
    TipoOperacion,
    UnidadMedida,
)
from core.erp.models import CabMovimiento, DetMovimiento
from core.erp.forms import CabMovimientoForm


class CabMovimientoListView(
    LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView
):
    model = CabMovimiento
    template_name = "cab_movimiento/list.html"
    permission_required = "erp.view_cab_movimiento"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "searchdata":
                data = []
                for i in CabMovimiento.objects.all():
                    data.append(i.toJSON())
            elif action == "search_details_prod":
                data = []
                for i in DetMovimiento.objects.filter(movimiento_id=request.POST["id"]):
                    data.append(i.toJSON())
                # movimiento = CabMovimiento.objects.get(pk=request.POST['id'])
                # data = [det.toJSON() for det in movimiento.detmovimiento_set.all()]
            else:
                data["error"] = "Ha ocurrido un error"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Listado de Movimientos de Stock"
        context["create_url"] = reverse_lazy("erp:cab_movimiento_create")
        context["list_url"] = reverse_lazy("erp:cab_movimiento_list")
        context["entity"] = "Movimientos de Stock"
        return context

class CabMovimientoCreateView(
    LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView
):
    model = CabMovimiento
    form_class = CabMovimientoForm
    template_name = "cab_movimiento/create.html"
    success_url = reverse_lazy("erp:cab_movimiento_list")
    permission_required = "erp.add_cab_movimiento"
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_products":
                data = []
                prods = Producto.objects.filter(
                    descripcion__icontains=request.POST["term"]
                )[0:10]
                for i in prods:
                    item = i.toJSON()
                    print(item)
                    item["producto"] = i.toJSON()
                    item["costo_mmnn"] = 0  # recuperar costo promedio del producto
                    item["costo_docu"] = 0  # recuperar costo promedio del producto
                    data.append(item)
            elif action == "add":
                with transaction.atomic():
                    vents = json.loads(request.POST["vents"])
                    max_numero = CabMovimiento.objects.filter(
                        tipo_operacion_id=vents["tipo_operacion"]
                    ).aggregate(Max("numero"))["numero__max"]
                    # Incrementar el número obtenido en 1 o usar 1 si no hay movimientos existentes
                    numero = max_numero + 1 if max_numero is not None else 1

                    movimiento = CabMovimiento()
                    movimiento.empresa_id = request.session.get("user_empresa_id")
                    movimiento.tipo_operacion_id = vents["tipo_operacion"]
                    movimiento.fecha = vents["fecha"]
                    movimiento.numero = numero
                    movimiento.deposito_id = vents["deposito"]
                    movimiento.observacion = vents["observacion"]
                    movimiento.save()

                    for i in vents["products"]:
                        max_item = DetMovimiento.objects.filter(
                            movimiento_id=movimiento.id
                        ).aggregate(Max("item"))["item__max"]
                        item = max_item + 1 if max_item is not None else 1
                        det = DetMovimiento()
                        det.movimiento_id = movimiento.id
                        det.item = item
                        det.producto_id = i["id"]
                        det.cantidad = int(i["cantidad"])
                        unidad_medida = i["unidad_medida"]
                        det.unidad_medida_id = unidad_medida["id"]
                        det.costo_mmnn = float(i["costo_mmnn"])
                        det.save()

                        #movimiento = agregar_movimiento_producto(
                        #    deposito_id=movimiento.deposito_id,  # vents['deposito'],
                        #    producto_id=det.producto_id,  # i['id'],
                        #    unidad_medida_id=det.unidad_medida_id,  # i['unidad_medida']['id'],
                        #    fecha=movimiento.fecha,  # vents['fecha'],
                        #    tipo_operacion_id=movimiento.tipo_operacion_id,  # vents['tipo_operacion']['id'],
                        #    cantidad=det.cantidad,  # int(i['cantidad'])
                        #)

            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Creación de Movimiento"
        context["entity"] = "Movimientos"
        context["list_url"] = self.success_url
        context["action"] = "add"
        context["det"] = []
        return context

class CabMovimientoUpdateView(
    LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView
):
    model = CabMovimiento
    form_class = CabMovimientoForm
    template_name = "cab_movimiento/create.html"
    success_url = reverse_lazy("erp:cab_movimiento_list")
    permission_required = "erp.change_cab_movimiento"
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST["action"]
            if action == "search_products":
                data = []
                prods = Producto.objects.filter(
                    descripcion__icontains=request.POST["term"]
                )[0:10]
                for i in prods:
                    item = i.toJSON()
                    # item['value'] = i.name
                    item["descripcion"] = i.descripcion
                    item["costo_mmnn"] = 0
                    data.append(item)
            elif action == "edit":
                with transaction.atomic():
                    vents = json.loads(request.POST["vents"])
                    print(vents)
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    movimiento = self.get_object()
                    movimiento.tipo_operacion_id = vents["tipo_operacion"]
                    movimiento.fecha = vents["fecha"]
                    movimiento.numero = vents["numero"]
                    movimiento.deposito_id = vents["deposito"]
                    movimiento.observacion = vents["observacion"]
                    movimiento.save()
                    movimiento.detmovimiento_set.all().delete()

                    for i in vents["products"]:
                        print('llega aqui')
                        det = DetMovimiento()
                        det.movimiento_id = movimiento.id
                        det.item = i['item']
                        det.producto_id = i["producto"]["id"]
                        det.unidad_medida_id = i["unidad_medida"]["id"]
                        det.cantidad = float(i["cantidad"])
                        det.costo_mmnn = float(i["costo_mmnn"])
                        det.costo_docu = float(i["costo_docu"])
                        det.save()
                    data = {"id": movimiento.id}
            else:
                data["error"] = "No ha ingresado a ninguna opción"
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetMovimiento.objects.filter(movimiento_id=self.get_object().id):
                print(i)
                #item = i.producto.toJSON()
                #item["descripcion"] = i.descripcion
                #item["categoria"] = i.categoria
                #item["unidad_medida"] = i.unidad_medida
                #item["cantidad"] = i.cantidad
                #item["costo_mmnn"] = 0
                #data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edición de un Movimiento"
        context["entity"] = "Movimientos"
        context["list_url"] = self.success_url
        context["action"] = "edit"
        # context['det'] = json.dumps(self.get_details_product())
        # Obtener el detalle de productos y serializarlo correctamente
        detalle_productos = []
        for det in self.object.detmovimiento_set.all():
            detalle_producto = det.toJSON()
            detalle_producto["cantidad"] = float(detalle_producto["cantidad"])
            detalle_producto["costo_mmnn"] = float(detalle_producto["costo_mmnn"])
            detalle_productos.append(detalle_producto)
        context["det"] = json.dumps(detalle_productos)

        return context

class  CabMovimientoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model =  CabMovimiento
    template_name = 'cab_movimiento/delete.html'
    success_url = reverse_lazy('erp:cab_movimiento_list')
    permission_required = 'erp.delete_cab_movimiento'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de un Movimiento'
        context['entity'] = 'Movimientos'
        context['list_url'] = self.success_url
        return context

## Actualizacion de saldo
def calcular_saldo_anterior(deposito_id, producto_id, fecha):
    # Obtener el último movimiento antes de la fecha proporcionada
    ultimo_movimiento = (
        MovimientoProductoFecha.objects.filter(
            deposito_id=deposito_id, producto_id=producto_id, fecha__lt=fecha
        )
        .order_by("-fecha")
        .first()
    )

    # Si hay un último movimiento, devolver su saldo, de lo contrario, devolver 0.0000
    return ultimo_movimiento.saldo if ultimo_movimiento else 0.0000

def movimiento_fecha(deposito_id, producto_id, fecha):
    mov = MovimientoProductoFecha.objects.get(
        deposito_id=deposito_id, producto_id=producto_id, fecha__lte=fecha
    )
    return mov if mov else None

def agregar_movimiento_producto(
    deposito_id, producto_id, unidad_medida_id, fecha, tipo_operacion_id, cantidad
):
    tipo_operacion = TipoOperacion.objects.get(id=tipo_operacion_id)
    mov = movimiento_fecha(deposito_id, producto_id, fecha)
    if mov is not None:
        mov.saldo_anterior = calcular_saldo_anterior(deposito_id, producto_id, fecha)
        if tipo_operacion.tipo == "S":
            mov.entrada += Decimal(cantidad)
        elif tipo_operacion.tipo == "R":
            mov.salida += Decimal(cantidad)
        else:
            raise ValueError("Tipo de operación no válido")
        mov.saldo = Decimal(mov.saldo_anterior) + mov.entrada - mov.salida
        mov.save()
        return mov
    else:
        saldo_anterior = calcular_saldo_anterior(deposito_id, producto_id, fecha)
        if tipo_operacion.tipo == "S":
            entrada = cantidad
            salida = 0
        elif tipo_operacion.tipo == "R":
            entrada = 0
            salida = cantidad
        else:
            raise ValueError("Tipo de operación no válido")
        saldo = saldo_anterior + entrada - salida
        # Crear el nuevo movimiento
        movimiento = MovimientoProductoFecha.objects.create(
            deposito_id=deposito_id,
            producto_id=producto_id,
            unidad_medida_id=unidad_medida_id,
            fecha=fecha,
            saldo_anterior=saldo_anterior,
            entrada=entrada,
            salida=salida,
            saldo=saldo,
        )
        return movimiento
