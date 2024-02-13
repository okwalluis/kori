from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.base.models import Persona
from core.base.forms import PersonaForm

class PersonaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Persona
    template_name = 'persona/list.html'
    permission_required = 'base.view_persona'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Persona.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Personas'
        context['create_url'] = reverse_lazy('base:persona_create')
        context['list_url'] = reverse_lazy('base:persona_list')
        context['entity'] = 'Personas'
        return context


class PersonaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/create.html'
    success_url = reverse_lazy('base:persona_list')
    permission_required = 'base.add_persona'
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
        context['title'] = 'Creación de una Persona'
        context['entity'] = 'Personas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PersonaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/create.html'
    success_url = reverse_lazy('base:persona_list')
    permission_required = 'base.change_persona'
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
        context['title'] = 'Edición de una Persona'
        context['entity'] = 'Personas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class PersonaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Persona
    template_name = 'persona/delete.html'
    success_url = reverse_lazy('base:persona_list')
    permission_required = 'base.delete_persona'
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
        context['title'] = 'Eliminación de una Persona'
        context['entity'] = 'Personas'
        context['list_url'] = self.success_url
        return context