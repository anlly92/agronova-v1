document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll('input[name="elemento"]');
    const campoOculto = document.getElementById("elemento_oculto");

    radios.forEach(radio => {
        radio.addEventListener("change", function () {
            campoOculto.value = this.value;
        });
    });
});
