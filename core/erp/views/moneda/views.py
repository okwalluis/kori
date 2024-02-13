from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Moneda
from core.erp.forms import MonedaForm


class MonedaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Moneda
    template_name = 'moneda/list.html'
    permission_required = 'erp.view_moneda'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Moneda.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Monedas'
        context['create_url'] = reverse_lazy('erp:moneda_create')
        context['list_url'] = reverse_lazy('erp:moneda_list')
        context['entity'] = 'Monedas'
        return context


class MonedaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Moneda
    form_class = MonedaForm
    template_name = 'moneda/create.html'
    success_url = reverse_lazy('erp:moneda_list')
    permission_required = 'erp.add_moneda'
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
        context['title'] = 'Creación un Moneda'
        context['entity'] = 'Monedas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class MonedaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Moneda
    form_class = MonedaForm
    template_name = 'moneda/create.html'
    success_url = reverse_lazy('erp:moneda_list')
    permission_required = 'erp.change_moneda'
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
        context['title'] = 'Edición un Moneda'
        context['entity'] = 'Monedas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class MonedaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Moneda
    template_name = 'moneda/delete.html'
    success_url = reverse_lazy('erp:moneda_list')
    permission_required = 'erp.delete_moneda'
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
        context['title'] = 'Eliminación de un Moneda'
        context['entity'] = 'Monedas'
        context['list_url'] = self.success_url
        return context
