  const btnEnviar = document.getElementById('btnEnviar');
  const formulario = document.getElementById('formularioIngreso');

  const modalConfirmar = new bootstrap.Modal(document.getElementById('confirmarModal'), {
    backdrop: 'static',
    keyboard: false
  });

  const modalExito = new bootstrap.Modal(document.getElementById('exitoModal'), {
    backdrop: 'static',
    keyboard: false
  });

  const modalAdvertencia = new bootstrap.Modal(document.getElementById('advertenciaModal'), {
    backdrop: 'static', // Impide cerrar al hacer clic fuera
    keyboard: false     // Impide cerrar con tecla Esc
});


  // Mostrar modal correspondiente al validar el formulario
  btnEnviar.addEventListener('click', function () {
    if (formulario.checkValidity()) {
      modalConfirmar.show(); // Mostrar confirmación si el formulario está completo
    } else {
      modalAdvertencia.show(); // Mostrar advertencia si faltan campos
    }
  });

  // Si confirma, cerrar modal y mostrar éxito, luego enviar formulario
  document.getElementById('btnConfirmar').addEventListener('click', function () {
    modalConfirmar.hide();
    setTimeout(() => {
      modalExito.show();
      setTimeout(() => {
        formulario.submit();
      }, 800);
    }, 400);
  });

  const registroExitoso = "{{ registro_exitoso|yesno:'true,false' }}";
  if (registroExitoso == true) {
    modalExito.show();
    setTimeout(() => {
      window.location.href = "{% url 'gestionar_administrador' %}";
    }, 3000);
  }

