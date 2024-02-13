from django.shortcuts import render, redirect

from core.base.models import Empresa, Sucursal


"""x
def vista_principal(request):
    # Obtener la información de la sesión
    empresa_id = request.session.get('empresa_id')
    sucursal_id = request.session.get('sucursal_id')

    # Obtener las instancias de Empresa y Sucursal
    empresa = Empresa.objects.get(pk=empresa_id)
    sucursal = Sucursal.objects.get(pk=sucursal_id)

    # Resto de la lógica de la vista...

    return render(request, 'template.html', {'empresa': empresa, 'sucursal': sucursal})
"""        