### get_context_data
Devuelve un diccionario que representa el contexto de la plantilla.
``` python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["number"] = random.randrange(1, 100)
    return context
```
### Dispatch
El método dispatch, se ejecuta al comienzo cuando se hace una llamada a una vista.
Se encarga de redireccionar de acuerdo al tipo de solicitud (POST o GET) que se haga.
La misma de puede sobreescribir
``` python
def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
```
### Decorators
Son funciones que añaden funcionalidades a otras funciones como las vistas basadas en clases.
``` python
from django.views.decorators.http import require_http_methods
...
    @login_required
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
``` 
### POST

### AJAX
Tecnología del tipo asíncrona. 


### LISTVIEW

### CREATEVIEW
vista que muestra un formulario para crear un objetoLista basada en clases

### MODELFORM
Para aplicaciones basadas en base de datos.
Permite evitar la redundacia de codigos ya que evita volver a definir los tipos de campos en los formularios, 
ya que se ha definido en el modelo.
Django proporciona una clase auxiliar que te permite crear una clase Form a partir de un modelo de Django.


## Propiedad Widget
nos permite personalizar un componente en el form.

## UPDATEVIEW
es una vista generica que se utiliza para editar registros

## TemplateView
se encarga de presentar un plantilla que se envia como parametro en template_name

## FORMVIEW
Es similar a create o update pero solo valida si el formulario es válido

## LOGINVIEW

## FORMVIEW
