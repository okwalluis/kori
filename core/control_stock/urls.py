from django.urls import path

from core.control_stock.views.categoria.views import CategoriaCreateView, CategoriaDeleteView, CategoriaListView, CategoriaUpdateView
from core.control_stock.views.subcategoria.views import SubCategoriaCreateView, SubCategoriaDeleteView, SubCategoriaListView, SubCategoriaUpdateView
from core.control_stock.views.unidad_medida.views import UnidadMedidaCreateView, UnidadMedidaDeleteView, UnidadMedidaListView, UnidadMedidaUpdateView
from core.control_stock.views.producto.views import ProductoCreateView, ProductoDeleteView, ProductoListView, ProductoUpdateView
from core.control_stock.views.tipo_operacion.views import TipoOperacionListView, TipoOperacionCreateView, TipoOperacionUpdateView, TipoOperacionDeleteView
from core.control_stock.views.conversion_medida.views import ConversionMedidaListView, ConversionMedidaCreateView, ConversionMedidaUpdateView, ConversionMedidaDeleteView

from core.control_stock.views.existencia_producto.views import ExistenciaProductoListView

app_name = 'control_stock'

urlpatterns = [
    path('categoria/list/', CategoriaListView.as_view(), name='categoria_list'),
    path('categoria/add/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categoria/update/<int:pk>/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categoria/delete/<int:pk>/', CategoriaDeleteView.as_view(), name='categoria_delete'),
    
    path('subcategoria/list/', SubCategoriaListView.as_view(), name='subcategoria_list'),
    path('subcategoria/add/', SubCategoriaCreateView.as_view(), name='subcategoria_create'),
    path('subcategoria/update/<int:pk>/', SubCategoriaUpdateView.as_view(), name='subcategoria_update'),
    path('subcategoria/delete/<int:pk>/', SubCategoriaDeleteView.as_view(), name='subcategoria_delete'),

    path('unidad_medida/list/', UnidadMedidaListView.as_view(), name='unidad_medida_list'),
    path('unidad_medida/add/', UnidadMedidaCreateView.as_view(), name='unidad_medida_create'),
    path('unidad_medida/update/<int:pk>/', UnidadMedidaUpdateView.as_view(), name='unidad_medida_update'),
    path('unidad_medida/delete/<int:pk>/', UnidadMedidaDeleteView.as_view(), name='unidad_medida_delete'),

    path('producto/list/', ProductoListView.as_view(), name='producto_list'),
    path('producto/add/', ProductoCreateView.as_view(), name='producto_create'),
    path('producto/update/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/delete/<int:pk>/', ProductoDeleteView.as_view(), name='producto_delete'),

    path('tipo_operacion/list/', TipoOperacionListView.as_view(), name='tipo_operacion_list'),
    path('tipo_operacion/add/', TipoOperacionCreateView.as_view(), name='tipo_operacion_create'),
    path('tipo_operacion/update/<int:pk>/', TipoOperacionUpdateView.as_view(), name='tipo_operacion_update'),
    path('tipo_operacion/delete/<int:pk>/', TipoOperacionDeleteView.as_view(), name='tipo_operacion_delete'),

    path('conversion_medida/list/', ConversionMedidaListView.as_view(), name='conversion_medida_list'),
    path('conversion_medida/add/', ConversionMedidaCreateView.as_view(), name='conversion_medida_create'),
    path('conversion_medida/update/<int:pk>/', ConversionMedidaUpdateView.as_view(), name='conversion_medida_update'),
    path('conversion_medida/delete/<int:pk>/', ConversionMedidaDeleteView.as_view(), name='conversion_medida_delete'),

    path('existencia_producto/list/', ExistenciaProductoListView.as_view(), name='existencia_producto_list'),

]