document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendario-js');
    const modalEliminar = document.getElementById('modal-eliminar');
    const inputIdEliminar = document.getElementById('id_evento_eliminar');
    const btnAbrirEliminar = document.getElementById('abrirModalEliminar');
    const btnCancelarEliminar = document.getElementById('btn-cancelar-eliminar');

    let eventoSeleccionado = null;

    if (calendarEl && window.FullCalendar) {
        window.miCalendario = new window.FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: '',
                center: '',
                right: ''
            },
            locale: 'es',
            height: 350,
            events: window.eventos,
            eventClick: function (info) {
                console.log("Evento clickeado:", info.event);

                const googleId = info.event.extendedProps.google_event_id;
                if (googleId) {
                    console.log("google_event_id encontrado:", googleId);
                    inputIdEliminar.value = googleId;
                    document.getElementById("id_evento_actualizar").value = googleId;
                    eventoSeleccionado = info.event;
                } else {
                    console.warn("No se encontró google_event_id en el evento.");
                }
            },
            
        });

        window.miCalendario.render();

        const currentTitle = window.miCalendario.view.title;
        document.getElementById('calendar-title').textContent = currentTitle;

        // Título dinámico
        window.miCalendario.on('datesSet', function (info) {
            document.getElementById('calendar-title').textContent = info.view.title;
        });

        document.getElementById('btn-prev').addEventListener('click', function () {
            window.miCalendario.prev();
        });

        document.getElementById('btn-next').addEventListener('click', function () {
            window.miCalendario.next();
        });

        
    }
    

    // Botón para abrir modal de eliminación
    if (btnAbrirEliminar) {
        btnAbrirEliminar.addEventListener('click', function () {
            if (inputIdEliminar.value) {
                console.log("Abriendo modal para eliminar tarea con ID:", inputIdEliminar.value);
                modalEliminar.style.display = 'block';
            } else {
                alert("Primero selecciona una tarea del calendario.");
            }
        });
    }

    // Cerrar modal
    if (btnCancelarEliminar) {
        btnCancelarEliminar.addEventListener('click', function () {
            modalEliminar.style.display = 'none';
            inputIdEliminar.value = '';
            eventoSeleccionado = null;
        });
    }
});
