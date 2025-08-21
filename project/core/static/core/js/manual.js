$(document).ready(function () {
  // Configuración inicial del libro (tamaño, animaciones y estilo de paso de página)
  $("#flipbook").turn({
    width: 1350,
    height: 800,
    autoCenter: true,
    gradients: true, 
    elevation: 30,      // altura de la "sombra" al pasar página
    duration: 900,     // tiempo que tarda en pasar la página (milisegundos)
    display: "double"   // dos páginas abiertas al mismo tiempo (como un libro real)
  });

  

  // Si haces clic en la parte derecha, avanza.
  $(document).on("click", "#flipbook .page", function (e) {
    const bookOffset = $("#flipbook").offset();
    const clickX = e.pageX - bookOffset.left;
    const bookWidth = $("#flipbook").width();

    if (clickX < bookWidth / 2) {
      $("#flipbook").turn("previous");
    } else {
      $("#flipbook").turn("next");
    }
  });

  // Función para que el índice sea clickeable:
  // Básicamente, si en el índice haces clic en "Introducción" (por ejemplo),
  // esto te manda a la página indicada en el libro.
  window.goToPage = function(pageNumber) {
    $("#flipbook").turn("page", pageNumber);
  };
});
