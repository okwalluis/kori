from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin

from core.control_stock.models import UnidadMedida
from core.control_stock.forms import UnidadMedidaForm

class UnidadMedidaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = UnidadMedida
    template_name = 'unidad_medida/list.html'
    permission_required = 'control_stock.view_unidad_medida'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in UnidadMedida.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Unidades de Medidas'
        context['create_url'] = reverse_lazy('control_stock:unidad_medida_create')
        context['list_url'] = reverse_lazy('control_stock:unidad_medida_list')
        context['entity'] = 'Unidades de Medidas'
        return context

class UnidadMedidaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'unidad_medida/create.html'
    success_url = reverse_lazy('control_stock:unidad_medida_list')
    permission_required = 'control_stock.add_unidad_medida'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Unidad de Medida'
        context['entity'] = 'Unidades de Medidas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class UnidadMedidaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = UnidadMedida
    form_class = UnidadMedidaForm
    template_name = 'unidad_medida/create.html'
    success_url = reverse_lazy('control_stock:unidad_medida_list')
    permission_required = 'control_stock.change_unidad_medida'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una Unidad de Medida'
        context['entity'] = 'Unidades de Medidas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class UnidadMedidaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = UnidadMedida
    template_name = 'unidad_medida/delete.html'
    success_url = reverse_lazy('control_stock:unidad_medida_list')
    permission_required = 'control_stock.delete_unidad_medida'
    url_redirect = success_url

    @method_decorator(login_required)
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
        context['title'] = 'Eliminación de una Unidad de Medida'
        context['entity'] = 'Unidades de Medidas'
        context['list_url'] = self.success_url
        return context