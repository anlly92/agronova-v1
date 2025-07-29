document.addEventListener('DOMContentLoaded', function () {
    // Animación del tractor
    lottie.loadAnimation({
        container: document.getElementById('lottie'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: 'https://assets6.lottiefiles.com/packages/lf20_4pdpfbjn.json'
    });

    // Animación de título letra por letra
    const titulo = document.querySelector('h1');
    const textoOriginal = titulo.textContent;
    titulo.textContent = ''; // Limpiar texto al inicio

    let index = 0;
    const velocidad = 300; // ms entre letras

    function mostrarLetra() {
        if (index < textoOriginal.length) {
            titulo.textContent += textoOriginal.charAt(index);
            index++;
            setTimeout(mostrarLetra, velocidad);
        }
    }

    // Esperar un poco antes de comenzar
    setTimeout(mostrarLetra, 800); // Puedes ajustar el delay según el inicio del tractor
});


