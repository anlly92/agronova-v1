from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import ( 
    PasswordResetView, PasswordResetConfirmView,
    PasswordChangeView,
    )
from django.urls import reverse_lazy

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect

def mostrar_home(request):
    return render (request,'core/home_principal.html')

def mostrar_login(request):
    return render ( request, 'core/login.html')

@login_required(login_url='login')
def mostrar_inicio(request):
    return render ( request, 'core/index_administrador.html')

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

