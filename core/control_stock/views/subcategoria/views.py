from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin

from core.control_stock.models import SubCategoria
from core.control_stock.forms import SubCategoriaForm

class SubCategoriaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = SubCategoria
    template_name = 'subcategoria/list.html'
    permission_required = 'control_stock.view_subcategoria'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in SubCategoria.objects.filter(empresa_id=request.session.get('user_empresa_id')):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de SubCategorías'
        context['create_url'] = reverse_lazy('control_stock:subcategoria_create')
        context['list_url'] = reverse_lazy('control_stock:subcategoria_list')
        context['entity'] = 'SubCategorías'
        return context

class SubCategoriaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'subcategoria/create.html'
    success_url = reverse_lazy('control_stock:subcategoria_list')
    permission_required = 'control_stock.add_subcategoria'
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
        context['title'] = 'Creación de una SubCategoría'
        context['entity'] = 'SubCategorías'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class SubCategoriaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = SubCategoria
    form_class = SubCategoriaForm
    template_name = 'subcategoria/create.html'
    success_url = reverse_lazy('control_stock:subcategoria_list')
    permission_required = 'control_stock.change_subcategoria'
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
        context['title'] = 'Edición de una SubCategoría'
        context['entity'] = 'SubCategorías'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class SubCategoriaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = SubCategoria
    template_name = 'subcategoria/delete.html'
    success_url = reverse_lazy('control_stock:subcategoria_list')
    permission_required = 'control_stock.delete_subcategoria'
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
        context['title'] = 'Eliminación de una SubCategoría'
        context['entity'] = 'SubCategorías'
        context['list_url'] = self.success_url
        return context