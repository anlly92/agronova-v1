# inventarios/utils.py
from datetime import datetime
import unicodedata


def parsear_fecha(fecha_str):
    formatos = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"]
    for formato in formatos:
        try:
            return datetime.strptime(fecha_str, formato).date()
        except ValueError:
            continue
    return None

def normalizar_texto(texto):
    """Elimina tildes y convierte a minúsculas para facilitar búsquedas."""
    texto = texto.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


def es_numero(valor):
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        return False





