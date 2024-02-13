from django.urls import path

from core.base.views.persona.views import *
from core.base.views.empresa.views import *
from core.base.views.pais.views import *
from core.base.views.sucursal.views import *
from core.base.views.deposito.views import *

app_name = 'base'

urlpatterns = [
    path('persona/list/', PersonaListView.as_view(), name='persona_list'),
    path('persona/add/', PersonaCreateView.as_view(), name='persona_create'),
    path('persona/update/<int:pk>/', PersonaUpdateView.as_view(), name='persona_update'),
    path('persona/delete/<int:pk>/', PersonaDeleteView.as_view(), name='persona_delete'),
    
    path('empresa/list/', EmpresaListView.as_view(), name='empresa_list'),
    path('empresa/add/', EmpresaCreateView.as_view(), name='empresa_create'),
    path('empresa/update/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_update'),
    path('empresa/delete/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_delete'),

    path('pais/list/', PaisListView.as_view(), name='pais_list'),
    path('pais/add/', PaisCreateView.as_view(), name='pais_create'),
    path('pais/update/<int:pk>/', PaisUpdateView.as_view(), name='pais_update'),
    path('pais/delete/<int:pk>/', PaisDeleteView.as_view(), name='pais_delete'),

    path('sucursal/list/', SucursalListView.as_view(), name='sucursal_list'),
    path('sucursal/add/', SucursalCreateView.as_view(), name='sucursal_create'),
    path('sucursal/update/<int:pk>/', SucursalUpdateView.as_view(), name='sucursal_update'),
    path('sucursal/delete/<int:pk>/', SucursalDeleteView.as_view(), name='sucursal_delete'),

    path('deposito/list/', DepositoListView.as_view(), name='deposito_list'),
    path('deposito/add/', DepositoCreateView.as_view(), name='deposito_create'),
    path('deposito/update/<int:pk>/', DepositoUpdateView.as_view(), name='deposito_update'),
    path('deposito/delete/<int:pk>/', DepositoDeleteView.as_view(), name='deposito_delete'),

]

