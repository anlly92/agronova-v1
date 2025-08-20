document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll('input[name="elemento"]');
    const campoOculto = document.getElementById("elemento_oculto");

    window.ids = []; 

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            const seleccionados = Array.from(checkboxes)
                .filter(c => c.checked)
                .map(c => c.value);
            campoOculto.value = seleccionados.join(",");

            window.ids = seleccionados;
            console.log("Elementos seleccionados:", window.ids); // opcional para depuración
        });
    });
});