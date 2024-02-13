from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from core.base.mixins import ValidatePermissionRequiredMixin

from core.erp.models import Concepto
from core.erp.forms import ConceptoForm


class ConceptoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Concepto
    template_name = 'concepto/list.html'
    permission_required = 'erp.view_concepto'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Concepto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Conceptos'
        context['create_url'] = reverse_lazy('erp:concepto_create')
        context['list_url'] = reverse_lazy('erp:concepto_list')
        context['entity'] = 'Conceptos'
        return context


class ConceptoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Concepto
    form_class = ConceptoForm
    template_name = 'concepto/create.html'
    success_url = reverse_lazy('erp:concepto_list')
    permission_required = 'erp.add_concepto'
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
        context['title'] = 'Creación un Concepto'
        context['entity'] = 'Conceptos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ConceptoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Concepto
    form_class = ConceptoForm
    template_name = 'concepto/create.html'
    success_url = reverse_lazy('erp:concepto_list')
    permission_required = 'erp.change_concepto'
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
        context['title'] = 'Edición un Concepto'
        context['entity'] = 'Conceptos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ConceptoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Concepto
    template_name = 'concepto/delete.html'
    success_url = reverse_lazy('erp:concepto_list')
    permission_required = 'erp.delete_concepto'
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
        context['title'] = 'Eliminación de un Concepto'
        context['entity'] = 'Conceptos'
        context['list_url'] = self.success_url
        return context
