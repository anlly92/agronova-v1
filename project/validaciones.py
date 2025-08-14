from datetime import  datetime
from django.apps import apps
from django.core.exceptions import FieldDoesNotExist
from cafe_cardamomo.models import Lote 
from inventarios.models import Inventario
import re
from django.core.exceptions import ObjectDoesNotExist

def validar_campos_especificos(post_data, modelo=None):
    errores = {}

    # --- Validaciones generales nombre ---
    nombre = post_data.get('nombre', '').strip()
    if nombre and not all(c.isalpha() or c.isspace() for c in nombre):
        errores['nombre'] = "⚠ El campo 'Nombre' solo debe contener letras y espacios."

    if Lote.objects.filter(nombre__iexact=nombre).exists():
        errores['nombre'] = "⚠ Ya existe ese nombre."

    # --- Validacion general de apellido ---
    apellido = post_data.get('apellido', '').strip()
    if apellido and not all(c.isalpha() or c.isspace() for c in apellido):
        errores['apellido'] = "⚠ El campo 'Apellido' solo debe contener letras y espacios."

    # --- Validacion general de telefono ---
    telefono = post_data.get('telefono', '').strip()
    if not telefono.isdigit():
        errores['telefono'] = "⚠ El campo 'Teléfono' solo debe contener números."
    elif len(telefono) < 10:
        errores['telefono'] = "⚠ El campo 'Teléfono' debe tener al menos 10 dígitos."

    # --- Validar ids de forma general ---
    for campo in post_data:
        if campo.startswith('id_'):
            valor = post_data.get(campo, '').strip()
            
            if valor.isdigit():

                if campo in ["id_admin", "id_empleado"]:
                    if len(valor) < 8 or len(valor) > 10:
                        errores[campo] = f"⚠ El campo '{campo.replace('_', ' ').title()}' debe tener al menos 10 dígitos."

                else:
                    if len(valor) > 5 :
                        errores[campo] = f"⚠ El campo '{campo.replace('_', ' ').title()}' debe tener al menos 5 dígitos."

            else:
                errores[campo] = f"⚠ El campo '{campo.replace('_', ' ').title()}' solo debe contener números."

            if modelo and modelo.objects.filter(**{campo: valor}).exists():
                errores[campo] = f"⚠ Ya existe un registro con este valor en '{campo.replace('_', ' ').title()}'."

    # --- Validar el tipo de empleado con su pago en el modulo empleado ----
    tipo_empleado = post_data.get('tipo_empleado', '').strip()
    pago_contrato = post_data.get('pago_contrato', '').strip()
    if tipo_empleado == 'Vinculado':
        if not pago_contrato:
            errores['pago_contrato'] = "⚠ El campo Pago por contrato es obligatorio para empleados vinculados."
        elif not pago_contrato.replace('.', '', 1).isdigit() or pago_contrato.count('.') > 1:
            errores['pago_contrato'] = "⚠ El campo Pago por contrato debe ser un número válido."
    elif tipo_empleado == 'No vinculado':
        if pago_contrato:
            errores['pago_contrato'] = "⚠ Los empleados no vinculados no deben registrar un pago por contrato."

    # --- Validaciones de lotes en hectareas  ---
    hectareas = post_data.get('hectareas', '').strip()
    if hectareas:
        if hectareas.replace('.', '', 1).isdigit():
            valor_hect = float(hectareas)
            if valor_hect < 1:
                errores['hectareas'] = "⚠ El valor de Hectáreas no puede ser menor a 0."
    else:
        errores['hectareas'] = "⚠ El valor ingresado en Hectáreas no es un número válido."


    # --- Validaciones específicas de recolección ---
    tipo_pago = post_data.get("tipo_pago", "").strip().capitalize()
    horas = post_data.get("horas_trabajadas", "").strip()
    kilos = post_data.get("kilos", "").strip()

    if tipo_pago == "Horas":
        if not horas or not horas.isdigit() or int(horas) <= 1:
            errores["horas_trabajadas"] = "⚠ Debes ingresar las horas trabajadas (mayor que 1)."
        if kilos:
            errores["kilos"] = "⚠ No debes llenar kilos si el tipo de pago es por horas."
    elif tipo_pago == "Kilos":
        if not kilos or not kilos.isdigit() or int(kilos) <= 1:
            errores["kilos"] = "⚠ Debes ingresar los kilos recolectados (mayor que 1)."
        if not horas or not horas.isdigit() or int(horas) <= 1:
            errores["horas_trabajadas"] = "⚠ También debes ingresar las horas trabajadas (mayor que 1) cuando el tipo de pago es por kilos."

    # --- Validar fecha ---
    # Verificar la fecha en otros ya que no me esta dando 
    fecha_str = post_data.get('fecha')
    try:
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hoy = datetime.today().date()
        if fecha > hoy:
            errores['fecha'] = 'La fecha no puede ser mayor que la actual.'
    except:
        pass  

    #--- Identificar el tipo de arbusto que es deacuerdo al id del lote ---
    id_lote = post_data.get('id_lote')
    tipo_producto = post_data.get('tipo_producto', '').strip()

    if id_lote and tipo_producto:
        try:
            lote = Lote.objects.get(id_lote=int(id_lote))
            tipo_arbusto_lote = lote.tipo_arbusto.strip()  # Cambiado de tipo_producto a tipo_arbusto

            if tipo_producto != tipo_arbusto_lote:
                errores['tipo_producto'] = f"⚠ El lote seleccionado solo permite recolección de {tipo_arbusto_lote}."

        except (Lote.DoesNotExist, ValueError):
            errores['id_lote'] = "⚠ El lote no existe o el ID no es válido."


    # --- No permitir la recoleccion en un lote inactivo ---
        
    id_lote = post_data.get("id_lote")
    if id_lote:
        try:
            lote = Lote.objects.get(id_lote=id_lote)

            if lote.estado.lower() != 'activo':
                errores['id_lote'] = 'No se puede registrar una recolección en un lote inactivo.'
            
        except Lote.DoesNotExist:
            errores['id_lote'] = 'El lote seleccionado no existe.'


    # ---Verificar que tipo de producto coinsida con el lote ---

    tipo_arbusto_form = post_data.get("tipo_producto", "").strip().lower()
    id_lote = post_data.get("id_lote")

    try:
        lote = Lote.objects.get(id_lote=id_lote)
        if lote and lote.tipo_arbusto.lower() != tipo_arbusto_form:
            errores["tipo_producto"] = f"El lote '{lote.nombre}' es para '{lote.tipo_arbusto}', no para '{tipo_arbusto_form}'."
    except Lote.DoesNotExist:
        errores["id_lote"] = "El lote no existe."



    # --- Validar correo ---
    correo = post_data.get('correo', '').strip()

    if correo:  # Solo validar si hay valor
        patron_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron_email, correo):
            errores['correo'] = "El correo electrónico no tiene un formato válido."

    return errores








