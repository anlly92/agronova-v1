from django.contrib.auth import views as auth_views
from django.urls import path
from core import views

urlpatterns = [
    path("", views.mostrar_home, name="home"),
    path("login/", auth_views.LoginView.as_view(
            template_name='core/login.html',
            redirect_authenticated_user=True
        ),name="login"),
    path("logout/", auth_views.LogoutView.as_view(
            next_page="home"
        ), name="logout"),
    path("inicio/", views.mostrar_inicio, name="inicio"),
    path("que_es_agronova/", views.que_es_agronova, name="que_es_agronova"),
    path("como_surgio_agronova/", views.como_surgio, name='como_surgio_agronova'),
    path("ventajas/", views.ventajas, name='ventajas'),
    path("mision_y_vision_agronova/", views.mision_y_vision_agronova, name='mision_y_vision_agronova'),
    path("historia/", views.historia, name='historia'),
    path("mision_y_vision_de_la_elisa/", views.mision_y_vision_elisa, name='mision_y_vision_la_elisa'),
    path("contraseña/", views.contraseña, name='contraseña'),
    path("terminos_condiciones/", views.terminos_condiciones, name='terminos_condiciones'),

    # el usuario ingresa su correo
    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="core/password_reset.html",
        email_template_name="core/password_reset_email.html",
        subject_template_name="core/password_reset_subject.txt",
        success_url="done/"),
        name="password_reset"),

    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="core/password_reset_done.html"),
        name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="core/password_reset_confirm.html",
        success_url="/reset/done/"),
        name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="core/password_reset_complete.html"),
        name="password_reset_complete"),

    # -----------------------  Cambiar contraseña estando logueado  -----------------------
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="core/password_change.html",
            success_url="done/"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="core/password_change_done.html"
        ),
        name="password_change_done",
    ),
]