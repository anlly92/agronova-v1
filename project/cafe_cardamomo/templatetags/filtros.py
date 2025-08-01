# cafe_cardamomo/templatetags/filtros.py

from django import template

register = template.Library()

@register.filter
def get_nombre_mes(valor):
    meses = {
        "1": "Enero", "2": "Febrero", "3": "Marzo", "4": "Abril",
        "5": "Mayo", "6": "Junio", "7": "Julio", "8": "Agosto",
        "9": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }
    return meses.get(str(valor), valor)
