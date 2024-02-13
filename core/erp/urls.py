from django.urls import path
from core.erp.views.dashboard.views import *
from core.erp.views.sale.views import *
from core.erp.views.tests.views import *

from core.erp.views.concepto.views import ConceptoCreateView, ConceptoDeleteView, ConceptoListView, ConceptoUpdateView
from core.erp.views.moneda.views import MonedaListView, MonedaCreateView, MonedaUpdateView, MonedaDeleteView
from core.erp.views.caja.views import CajaListView, CajaUpdateView, CajaCreateView, CajaDeleteView
from core.erp.views.cab_movimiento.views import CabMovimientoListView, CabMovimientoCreateView, CabMovimientoUpdateView, CabMovimientoDeleteView

app_name = 'erp'

urlpatterns = [
    
    # concepto
    path('concepto/list/', ConceptoListView.as_view(), name='concepto_list'),
    path('concepto/add/', ConceptoCreateView.as_view(), name='concepto_create'),
    path('concepto/update/<int:pk>/', ConceptoUpdateView.as_view(), name='concepto_update'),
    path('concepto/delete/<int:pk>/', ConceptoDeleteView.as_view(), name='concepto_delete'),
    # Moneda
    path('moneda/list/', MonedaListView.as_view(), name='moneda_list'),
    path('moneda/add/', MonedaCreateView.as_view(), name='moneda_create'),
    path('moneda/update/<int:pk>/', MonedaUpdateView.as_view(), name='moneda_update'),
    path('moneda/delete/<int:pk>/', MonedaDeleteView.as_view(), name='moneda_delete'),
    # caja
    path('caja/list/', CajaListView.as_view(), name='caja_list'),
    path('caja/add/', CajaCreateView.as_view(), name='caja_create'),
    path('caja/update/<int:pk>/', CajaUpdateView.as_view(), name='caja_update'),
    path('caja/delete/<int:pk>/', CajaDeleteView.as_view(), name='caja_delete'),
    
    # movimiento
    path('cab_movimiento/list/', CabMovimientoListView.as_view(), name='cab_movimiento_list'),
    path('cab_movimiento/add/', CabMovimientoCreateView.as_view(), name='cab_movimiento_create'),
    path('cab_movimiento/update/<int:pk>/', CabMovimientoUpdateView.as_view(), name='cab_movimiento_update'),
    path('cab_movimiento/delete/<int:pk>/', CabMovimientoDeleteView.as_view(), name='cab_movimiento_delete'),

    
    # home
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # sale
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_invoice_pdf'),
]

