/*  modales.js  (único para todo el sitio)  */
document.addEventListener("DOMContentLoaded", () => {
  /* ---------- capturas globales ---------- */
  const formulario      = document.getElementById("formularioIngreso");
  const btnEnviar       = document.getElementById("btnEnviar");

  const exitoEl         = document.getElementById("exitoModal");
  const advertenciaEl   = document.getElementById("advertenciaModal");
  const confirmarEl     = document.getElementById("confirmarModal");
  const btnConfirmar    = document.getElementById("btnConfirmar");

  /* ---------- instancias (solo si existen) ---------- */
  const modalExito       = exitoEl       ? new bootstrap.Modal(exitoEl)         : null;
  const modalAdvertencia = advertenciaEl ? new bootstrap.Modal(advertenciaEl)   : null;
  const modalConfirmar   = confirmarEl   ? new bootstrap.Modal(confirmarEl)     : null;

  /* ---------- 1) mostrar modal de éxito proveniente del backend ---------- */
  /* backend >  template:   {% if request.GET.sent %}<script>mostrarModal="true";</script>{% endif %} */
  if (typeof mostrarModal !== "undefined" && mostrarModal === "true" && modalExito) {
    modalExito.show();

    /* redirección opcional solo cuando lo definas en la plantilla */
    if (typeof redirLogin !== "undefined" && redirLogin === "true") {
      setTimeout(() => (window.location.href = "/login/"), 3000);
    }
  }

  /* ---------- 2) validación del envío ---------- */
  if (btnEnviar && formulario) {
    btnEnviar.addEventListener("click", () => {
      /* formulario.checkValidity() funciona en *cualquier* formulario con HTML5  */
      if (formulario.checkValidity()) {
        
        /* a) Hay modalConfirmar ⇒ ventana “¿Estás seguro?” */
        if (modalConfirmar) {
          modalConfirmar.show();
        }
        /* b) No hay confirmación ⇒ enviamos directo                */
        else { 
          formulario.submit();
        }
      } else {
        /* formulario incompleto ⇒ advertimos solo si existe modalAdvertencia */
        modalAdvertencia ? modalAdvertencia.show() : formulario.reportValidity();
      }
    });
  }

  /* ---------- 3) clic en “Sí, continuar” de la ventana Confirmar ---------- */
  if (btnConfirmar && modalConfirmar) {
      btnConfirmar.addEventListener("click", () => {
      modalConfirmar.hide();

      /* Esperamos transición, luego modal de éxito si existe */
      setTimeout(() => {
        formulario.submit();// <‑‑ finalmente se envía
      }, 400);
    });
  }
});