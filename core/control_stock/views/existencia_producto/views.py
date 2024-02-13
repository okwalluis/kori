from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.control_stock.models import ExistenciaProducto

class ExistenciaProductoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = ExistenciaProducto
    template_name = 'existencia_producto/list.html'
    permission_required = 'control_stock.view_existencia_producto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ExistenciaProducto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Existencia de producto'
        context['create_url'] = reverse_lazy('control_stock:existencia_producto_list')
        context['list_url'] = reverse_lazy('control_stock:existencia_producto_list')
        context['entity'] = 'Categoria'
        return context