document.addEventListener("DOMContentLoaded", function () {
    const campoFecha = document.getElementById("fecha");
    const iconoCalendario = document.getElementById("icono-calendario");

    if (campoFecha) {
        const picker = flatpickr(campoFecha, {
            dateFormat: 'Y-m-d',
            locale: "es",
        });

        if (iconoCalendario) {
            iconoCalendario.addEventListener("click", function () {
                picker.open();
            });
        }
    }
});