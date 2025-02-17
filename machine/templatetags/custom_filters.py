from django import template

# Registrar a biblioteca de filtros
register = template.Library()


# Definir um filtro personalizado para multiplicação
@register.filter(name='multiplicar')
def multiplicar(value, arg):
    return round(value * arg / 100, 2)

