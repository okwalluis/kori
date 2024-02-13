from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.base.models import Pais
from core.base.forms import PaisForm

class PaisListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Pais
    template_name = 'pais/list.html'
    permission_required = 'base.view_pais'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pais.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Países'
        context['create_url'] = reverse_lazy('base:pais_create')
        context['list_url'] = reverse_lazy('base:pais_list')
        context['entity'] = 'Países'
        return context


class PaisCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Pais
    form_class = PaisForm
    template_name = 'pais/create.html'
    success_url = reverse_lazy('base:pais_list')
    permission_required = 'base.add_pais'
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
        context['title'] = 'Creación de un País'
        context['entity'] = 'Países'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PaisUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Pais
    form_class = PaisForm
    template_name = 'pais/create.html'
    success_url = reverse_lazy('base:pais_list')
    permission_required = 'base.change_pais'
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
        context['title'] = 'Edición de una País'
        context['entity'] = 'Países'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PaisDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Pais
    template_name = 'pais/delete.html'
    success_url = reverse_lazy('base:pais_list')
    permission_required = 'base.delete_pais'
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
        context['title'] = 'Eliminación de una País'
        context['entity'] = 'Países'
        context['list_url'] = self.success_url
        return context