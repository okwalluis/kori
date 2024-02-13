from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.base.mixins import ValidatePermissionRequiredMixin

from core.base.models import Deposito
from core.base.forms import DepositoForm

class DepositoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Deposito
    template_name = 'deposito/list.html'
    permission_required = 'base.view_deposito'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Deposito.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Depositos'
        context['create_url'] = reverse_lazy('base:deposito_create')
        context['list_url'] = reverse_lazy('base:deposito_list')
        context['entity'] = 'Depositos'
        return context


class DepositoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Deposito
    form_class = DepositoForm
    template_name = 'deposito/create.html'
    success_url = reverse_lazy('base:deposito_list')
    permission_required = 'base.add_deposito'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                #data = form.save()
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
        context['title'] = 'Creación de un Depósito'
        context['entity'] = 'Depositos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class DepositoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Deposito
    form_class = DepositoForm
    template_name = 'deposito/create.html'
    success_url = reverse_lazy('base:deposito_list')
    permission_required = 'base.change_deposito'
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
        context['title'] = 'Edición de un Depósito'
        context['entity'] = 'Depósitos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class DepositoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Deposito
    template_name = 'deposito/delete.html'
    success_url = reverse_lazy('base:deposito_list')
    permission_required = 'base.delete_deposito'
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
        context['title'] = 'Eliminación de un Depósito'
        context['entity'] = 'Depósitos'
        context['list_url'] = self.success_url
        return context