from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin

from core.erp.models import Caja
from core.erp.forms import CajaForm

class CajaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Caja
    template_name = 'caja/list.html'
    permission_required = 'erp.view_caja'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Caja.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Cajas'
        context['create_url'] = reverse_lazy('erp:caja_create')
        context['list_url'] = reverse_lazy('erp:caja_list')
        context['entity'] = 'Cajas'
        return context


class CajaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'caja/create.html'
    success_url = reverse_lazy('erp:caja_list')
    permission_required = 'erp.add_caja'
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
        context['title'] = 'Creación de un Caja'
        context['entity'] = 'Cajas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class CajaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'caja/create.html'
    success_url = reverse_lazy('erp:caja_list')
    permission_required = 'erp.change_caja'
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
        context['title'] = 'Edición de un Caja'
        context['entity'] = 'Cajas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class CajaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Caja
    template_name = 'caja/delete.html'
    success_url = reverse_lazy('erp:caja_list')
    permission_required = 'erp.delete_caja'
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
        context['title'] = 'Eliminación de un Caja'
        context['entity'] = 'Cajas'
        context['list_url'] = self.success_url
        return context
