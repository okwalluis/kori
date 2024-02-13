#from config.wsgi import *
#from core.erp.models import Type
# lista

# query = Type.objects.all()
# print(query)

# inserción
# t = Type()
# t.name = 'Accionistas'
# t.save()

# edición
# t = Type.objects.get(id=1)
# print(t)

# eliminación
# t = Type.objects.get(pk=1)
# t.delete()

# obj = Type.objects.filter(name__contains='Acci')
# print(obj)
#
#obj = Type.objects.filter(name__icontains='Acci')
#print(obj)

from config.wsgi import *
from core.erp.models import *
import random

data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos',
        'Verduras y Hortalizas', 'Frutas', 'Cereales y derivados, azúcar y dulces',
        'Grasas, aceite y mantequilla']

# delete from public.erp_category;
# ALTER SEQUENCE erp_category_id_seq RESTART WITH 1;

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']

for i in range(1, 6000):
    name = ''.join(random.choices(letters, k=5))
    while Category.objects.filter(name=name).exists():
        name = ''.join(random.choices(letters, k=5))
    Category(name=name).save()
    print('Guardado registro {}'.format(i))
