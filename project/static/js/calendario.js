// Flatpickr en español
document.addEventListener("DOMContentLoaded", function () {
    const campoFecha = document.getElementById("fecha");
    const iconoCalendario = document.getElementById("icono-calendario");

    if (campoFecha) {
        flatpickr("#fecha", {
            dateFormat: "d/m/Y",
            locale: "es"
        });

        // Abre el calendario Flatpickr al hacer clic en el ícono
        if (iconoCalendario && campoFecha._flatpickr) {
            iconoCalendario.addEventListener("click", function () {
                campoFecha._flatpickr.open();
            });
        }
    }
});

// OPCIÓN 2: jQuery + Bootstrap Datepicker
$(document).ready(function () {
    // Inicializa el Bootstrap Datepicker en el input con ID "datepicker"
    $('#datepicker').datepicker({
        format: 'dd/mm/yyyy',         // Formato de fecha
        autoclose: true,              // Cierra automáticamente al elegir fecha
        todayHighlight: true,         // Resalta el día actual
        language: 'es',               // Idioma español
        endDate: new Date()           // No permite fechas futuras
    }).datepicker('setDate', new Date()); // Fecha por defecto: hoy

    // Mostrar el calendario al hacer clic en el ícono
    $('#icono-calendario').on('click', function () {
        $('#datepicker').datepicker('show');
    });
});