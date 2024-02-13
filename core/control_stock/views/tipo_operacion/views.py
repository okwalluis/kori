from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin

from core.control_stock.forms import TipoOperacionForm
from core.control_stock.models import TipoOperacion
from core.base.models import Empresa

class TipoOperacionListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = TipoOperacion
    template_name = 'tipo_operacion/list.html'
    permission_required = 'control_stock.view_tipo_operacion'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in TipoOperacion.objects.filter(empresa_id=request.session.get('user_empresa_id')):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Tipos de Operaciones'
        context['create_url'] = reverse_lazy('control_stock:tipo_operacion_create')
        context['list_url'] = reverse_lazy('control_stock:tipo_operacion_list')
        context['entity'] = 'Tipo Operación'
        return context

class TipoOperacionCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = TipoOperacion
    form_class = TipoOperacionForm
    template_name = 'tipo_operacion/create.html'
    success_url = reverse_lazy('control_stock:tipo_operacion_list')
    permission_required = 'control_stock.add_tipo_operacion'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    #asignacion de valor al campo empresa. Seria la empresa en la cual esta conectado el usuario.
                    empresa_id = request.session.get('user_empresa_id')
                    #falta asignar usuario que crea el registro
                    data = form.save(commit=True, empresa_id=empresa_id)
                else:
                    data['error'] = str(form.errors)
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Tipo de Operación'
        context['entity'] = 'Tipo de Operación'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class TipoOperacionUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = TipoOperacion
    form_class = TipoOperacionForm
    template_name = 'tipo_operacion/create.html'
    success_url = reverse_lazy('control_stock:tipo_operacion_list')
    permission_required = 'control_stock.change_tipo_operacion'
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
        context['title'] = 'Edición de un Tipo de Operación'
        context['entity'] = 'Tipo de Operación'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class TipoOperacionDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = TipoOperacion
    template_name = 'tipo_operacion/delete.html'
    success_url = reverse_lazy('control_stock:tipo_operacion_list')
    permission_required = 'control_stock.delete_tipo_operacion'
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
        context['title'] = 'Eliminación de un Tipo de Operación'
        context['entity'] = 'Tipo de Operación'
        context['list_url'] = self.success_url
        return context