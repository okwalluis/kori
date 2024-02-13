from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.base.mixins import ValidatePermissionRequiredMixin
from core.control_stock.models import ConversionMedida
from core.control_stock.forms import ConversionMedidaForm

class ConversionMedidaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = ConversionMedida
    template_name = 'conversion_medida/list.html'
    permission_required = 'control_stock.view_conversion_medida'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in ConversionMedida.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Conversiones de Medidas'
        context['create_url'] = reverse_lazy('control_stock:conversion_medida_create')
        context['list_url'] = reverse_lazy('control_stock:conversion_medida_list')
        context['entity'] = 'Conversión Medida'
        return context

class ConversionMedidaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = ConversionMedida
    form_class = ConversionMedidaForm
    template_name = 'conversion_medida/create.html'
    success_url = reverse_lazy('control_stock:conversion_medida_list')
    permission_required = 'control_stock.add_conversion_medida'
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
        context['title'] = 'Creación de una Conversión de Medida'
        context['entity'] = 'Conversión de Medida'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class ConversionMedidaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = ConversionMedida
    form_class = ConversionMedidaForm
    template_name = 'conversion_medida/create.html'
    success_url = reverse_lazy('control_stock:conversion_medida_list')
    permission_required = 'control_stock.change_conversion_medida'
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
        context['title'] = 'Edición de una Conversión de Medida'
        context['entity'] = 'Conversión de Medida'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class ConversionMedidaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = ConversionMedida
    template_name = 'conversion_medida/delete.html'
    success_url = reverse_lazy('control_stock:conversion_medida_list')
    permission_required = 'control_stock.delete_conversion_medida'
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
        context['title'] = 'Eliminación de una Conversión de Medida'
        context['entity'] = 'Conversión de Medida'
        context['list_url'] = self.success_url
        return context