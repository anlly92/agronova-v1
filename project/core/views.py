import traceback
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import ( PasswordResetView, PasswordResetConfirmView,PasswordChangeView )
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .quickstart import crear_evento,eliminar_evento,actualizar_evento
from core.paneles import (
    produccion_mensual,
    agroquimicos_mas_usados,
    producto_mas_vendido,
    finanzas_del_mes,
    obtener_alertas,
    cantidad_de_empleados,
    recoleccion_mensual_grafico,
    calendario_de_tareas,
)

def mostrar_home(request):
    return render (request,'core/home_principal.html')

def pantalla_carga(request):
    return render(request, "core/carga.html") # nueva

def mostrar_login(request):
    return render ( request, 'core/login.html')

@login_required(login_url='login')
def mostrar_inicio(request):
    produccion, mes_actual = produccion_mensual()
    agroquimicos, nombre_mes = agroquimicos_mas_usados()
    productos_vendidos, mes_ventas = producto_mas_vendido()
    finanzas, mes_finanzas = finanzas_del_mes()
    alertas = obtener_alertas()
    empleados = cantidad_de_empleados()
    grafico= recoleccion_mensual_grafico()
    eventos = calendario_de_tareas()
    context = {
        'produccion': produccion,
        'mes_actual': mes_actual,
        'agroquimicos': agroquimicos,
        'nombre_mes': nombre_mes,
        'productos_vendidos': productos_vendidos,
        'mes_ventas': mes_ventas,
        'finanzas': finanzas,
        'mes_finanzas': mes_finanzas,
        'alertas': alertas[:1],
        'alertas_extra': alertas,
        'empleados': empleados,
        'grafico':grafico,
        "eventos": eventos,
    }
    return render ( request, 'core/index_administrador.html',context)

def que_es_agronova (request):
    return render (request, 'core/que_es_agronova.html')

def como_surgio (request):
    return render (request, 'core/como_surgio.html')

def ventajas (request):
    return render (request, 'core/ventajas.html')

def mision_y_vision_agronova (request):
    return render (request, 'core/mision_agronova.html')

def historia (request):
    return render (request, 'core/historia.html')

def mision_y_vision_elisa (request):
    return render (request, 'core/mision_elisa.html')

def contraseña (request):
    return render (request, 'core/contraseña.html')

def terminos_condiciones (request):
    return render (request, 'core/terminos_condiciones.html')

def crear_evento_google_view(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        print("Inicio:", fecha_inicio)
        print("Fin:", fecha_fin)

        try:
            crear_evento(titulo, descripcion, fecha_inicio, fecha_fin)
            messages.success(request, "Evento creado correctamente en Google Calendar.")
        except Exception as e:
            messages.error(request, f"Error al crear evento: {str(e)}")

        return redirect('inicio')  # o donde debas redirigir
    else:
        return HttpResponse("Método no permitido",status=405)  

@csrf_exempt
def eliminar_evento_google_view(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        if not event_id:
            messages.error(request, "ID de evento no proporcionado.")
            return redirect("inicio")

        try:
            eliminar_evento(event_id)
            messages.success(request, "Evento eliminado correctamente.")
            return redirect("inicio")

        except Exception as e:
            messages.error(request, f"Error al eliminar evento: {str(e)}")
            return redirect("inicio")

    else:
        return redirect("inicio")

@csrf_exempt
def actualizar_evento_google_view(request):
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")

        try:
            actualizar_evento(event_id, titulo, descripcion, fecha_inicio, fecha_fin)
            return redirect("inicio")
        except Exception as e:
            return redirect("inicio")

class PasswordResetNoRedirectView(PasswordResetView):
    template_name = "core/contraseña.html"
    email_template_name = "core/password_reset_email.html"
    subject_template_name = "core/password_reset_subject.txt"

    def get_success_url(self):
        return reverse_lazy("password_reset") + "?sent=1"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        for user in form.get_users(email):
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(self.request).domain

            context = {
                "email": email,
                "uid": uid,
                "token": token,
                "domain": domain,
                "protocol": "https" if self.request.is_secure() else "http",
            }

            subject = render_to_string(self.subject_template_name, context).strip()
            html_message = render_to_string(self.email_template_name, context)
            text_message = strip_tags(html_message)

            msg = EmailMultiAlternatives(subject, text_message, None, [email])
            msg.attach_alternative(html_message, "text/html")
            msg.send()

        # Evita llamar a super().form_valid(form) para que no se envíe el correo duplicado
        return HttpResponseRedirect(self.get_success_url())

class PasswordResetConfirmNoRedirectView(PasswordResetConfirmView):
    template_name = "core/password_reset_confirm.html"
    def form_valid(self, form):
        # 1) Cambia la contraseña:
        form.save()

        # 2) Prepara contexto con la bandera
        context = self.get_context_data(**self.kwargs)
        context["ok"] = True                     # ← tu JS lo usará

        return render(self.request, self.template_name, context)

class PasswordChangeNoRedirectView(PasswordChangeView):
    template_name = "core/password_change.html"
    def form_valid(self, form):
        # 1) Cambia la contraseña:
        form.save()
        # 2) Prepara contexto con la bandera
        context = self.get_context_data(**self.kwargs)
        context["ok"] = True                     # ← tu JS lo usará
        return render(self.request, self.template_name, context)




