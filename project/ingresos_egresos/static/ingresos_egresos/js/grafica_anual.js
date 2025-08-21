document.addEventListener('DOMContentLoaded', function () {
    // Escucha el evento 'DOMContentLoaded' para asegurarse de que el DOM esté completamente cargado antes de ejecutar el código.
    const canvas = document.getElementById('verAnual');
    const btnCalendario = document.getElementById('Calendario');
    const btnDescargar = document.getElementById('descargarBtn');
    const btnDescargarGrafica = document.getElementById('descargarGrafica');
    const btnDescargarDatos = document.getElementById('descargarDatos');
    const submenuDescarga = document.getElementById('submenuDescarga');
    let chart;
    // Declara variables para el elemento canvas (con id 'verAnual'), los botones 'Calendario' y 'descargarGrafica', y una variable 'chart' para almacenar la instancia de la gráfica.

    
    // Verificar que los elementos existan
    if (!canvas) {
        console.error("Falta el elemento canvas en el HTML.");
        return;
    }
    // Comprueba si el elemento canvas con id 'verAnual' existe. Si no, muestra un error en la consola y detiene la ejecución.

    const ctx = canvas.getContext('2d');
    // Obtiene el contexto 2D del canvas para dibujar la gráfica.

    function obtenerNombreMes(numeroMes) {
        const meses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        
        return meses[numeroMes - 1];
    }

    
    function cargarGrafica(anio = new Date().getFullYear().toString()) {
        console.log("Cargando gráfica para el año:", anio); // Depuración
        // Define una función para cargar la gráfica, con un parámetro 'anio' que por defecto es el año actual como string (ej. "2025").

        // Validación del año
        if (!anio || isNaN(anio) || anio.length !== 4) {
            console.error("Año inválido:", anio);
            alert("Por favor, ingresa un año válido de 4 dígitos.");
            return;
        }
        // Valida que el año no esté vacío, sea un número y tenga exactamente 4 dígitos. Si no cumple, muestra un error y detiene la función.

        const url = `/ingresos_egresos/informe_anual/?anio=${anio}`;
        console.log("Enviando solicitud a:", url); // Depuración
        // Construye la URL para la solicitud fetch, usando la ruta '/ingresos_egresos/informe_anual/' con el parámetro 'anio'.

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(`Error ${response.status}: ${errorData.error || 'Error desconocido'}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log("Datos recibidos del servidor:", data); 
                if (!data.labels || !data.data || !data.data.ingresos || !data.data.egresos) {
                    throw new Error("Datos incompletos en la respuesta: " + JSON.stringify(data));
                }
                // Realiza una solicitud GET a la URL. Si la respuesta no es ok (status != 200), intenta parsear un mensaje de error. Si es ok, parsea los datos JSON.
                // Verifica que la respuesta contenga las claves esperadas ('labels', 'data', 'ingresos', 'egresos'). Si no, lanza un error.

                if (chart) chart.destroy();
                // Destruye la instancia anterior de la gráfica si existe, para evitar superposiciones.

                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: `Ingresos ${anio}`,
                                data: data.data.ingresos,
                                backgroundColor: '#2e7d32',
                                borderColor: '#1b5e20',
                                borderWidth: 1
                            },
                            {
                                label: `Egresos ${anio}`,
                                data: data.data.egresos,
                                backgroundColor: '#c62828',
                                borderColor: '#8e0000',
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            title: {
                                display: true,
                                text: `Ingresos y Egresos del año ${anio}`, // Aquí usamos el año dinámico
                                font: {
                                    size: 18,
                                    weight: 'bold'
                                },
                                padding: {
                                    top: 20,
                                    bottom: 15
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
                // Crea una nueva gráfica de barras con Chart.js, usando los datos recibidos.
                // Configura dos conjuntos de datos: 'Ingresos' (verde) y 'Egresos' (rojo), con etiquetas y valores del backend.
                // Opciones: gráfica responsiva y eje Y que comienza en cero.

                if (data.warning) {
                    console.warn("Advertencia del servidor:", data.warning);
                    alert(data.warning);
                }
                // Si la respuesta incluye una advertencia, la muestra en la consola y en un alert.
            })
            .catch(error => {
                console.error('Error en fetch:', error);
                alert("Error al cargar los datos de la gráfica: " + error.message);
            });
        // Captura y maneja cualquier error durante el fetch o el procesamiento de datos, mostrando un mensaje al usuario.
    }

    // Cargar gráfica inicial con el año actual
    console.log("Cargando gráfica inicial para el año:", new Date().getFullYear());
    cargarGrafica();
    // Llama a la función cargarGrafica con el año actual al cargar la página, y registra el proceso en la consola.

    // Crear ventana emergente
    const ventana = document.createElement("div");
    ventana.className = "ventana-calendario";
    ventana.style.display = "none";
    // Crea dinámicamente un div para el modal, con clase 'ventana-calendario' y oculto por defecto.

    const label = document.createElement("label");
    label.textContent = "Selecciona un año:";
    // Crea un elemento label para indicar al usuario que seleccione un año.

    const select = document.createElement("select");
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= currentYear - 4; year--) { // Limitar a 4 años atrás
        const option = document.createElement("option");
        option.value = year;
        option.textContent = year;
        select.appendChild(option);
    }
    select.value = currentYear;
    // Crea un elemento select con opciones de años desde el actual hasta 50 años atrás, seleccionando el año actual por defecto.

    const btnVer = document.createElement("button");
    btnVer.textContent = "Ver";

    const btnCerrar = document.createElement("button");
    btnCerrar.textContent = "Cerrar";

    // Contenedor para los botones
    const botonesContenedor = document.createElement("div");
    botonesContenedor.className = "botones-contenedor";
    botonesContenedor.style.display = "flex";
    botonesContenedor.style.justifyContent = "center";
    botonesContenedor.style.gap = "100px";
    botonesContenedor.appendChild(btnVer);
    botonesContenedor.appendChild(btnCerrar);

    // Depuración para verificar el centrado
    console.log("Estilo de justifyContent:", getComputedStyle(botonesContenedor).justifyContent);

    // Agregar select de mes
    const labelMes = document.createElement('label');
    labelMes.textContent = 'Selecciona un mes:';
    const selectMes = document.createElement('select');
    const meses = [
        { value: 1, text: 'Enero' },
        { value: 2, text: 'Febrero' },
        { value: 3, text: 'Marzo' },
        { value: 4, text: 'Abril' },
        { value: 5, text: 'Mayo' },
        { value: 6, text: 'Junio' },
        { value: 7, text: 'Julio' },
        { value: 8, text: 'Agosto' },
        { value: 9, text: 'Septiembre' },
        { value: 10, text: 'Octubre' },
        { value: 11, text: 'Noviembre' },
        { value: 12, text: 'Diciembre' }
    ];
    meses.forEach(mes => {
        const option = document.createElement('option');
        option.value = mes.value;
        option.textContent = mes.text;
        selectMes.appendChild(option);
    });
    selectMes.value = (new Date().getMonth() + 1).toString();

    ventana.appendChild(labelMes);
    ventana.appendChild(selectMes);
    ventana.appendChild(label);
    ventana.appendChild(select);
    ventana.appendChild(botonesContenedor);
    document.body.appendChild(ventana);
    // Agrega todos los elementos al modal y lo inserta en el body, usando un contenedor para los botones.

    // Posicionar ventana debajo de #Calendario y luego centrar
    function posicionarVentana() {
        const rect = btnCalendario.getBoundingClientRect();
        const ventanaWidth = ventana.offsetWidth || 300;
        const ventanaHeight = ventana.offsetHeight || 300;

        // Establece los estilos iniciales
        ventana.style.position = "fixed";
        ventana.style.top = (rect.bottom + window.scrollY + 10) + "px";
        ventana.style.left = (rect.left + window.scrollX + (rect.width - ventanaWidth) / 2) + "px";
        ventana.style.minWidth = "300px";
        ventana.style.transition = "all 0.3s ease";

        // Centra la ventana después de un delay
        setTimeout(() => {
            ventana.style.top = "50%";
            ventana.style.left = "50%";
            ventana.style.transform = "translate(-50%, -50%)";
        }, 50); // Aumentamos a 50ms para dar tiempo a la renderización
    }
    // Define una función para posicionar el modal inicialmente debajo del botón Calendario y luego centrarlo con transición.

    // Mostrar u ocultar ventana con #Calendario
    btnCalendario.addEventListener("click", function (e) {
        e.stopPropagation();
        posicionarVentana();
        ventana.style.display = ventana.style.display === "block" ? "none" : "block";
    });
    

    // Actualizar gráfica con el año seleccionado
    btnVer.addEventListener("click", function () {
        const anio = select.value;
        cargarGrafica(anio);
        ventana.style.display = "none";
    });
    // Asigna un evento click al botón Ver. Obtiene el año seleccionado, llama a cargarGrafica, y cierra el modal.

    // Cerrar ventana
    btnCerrar.addEventListener("click", function () {
        ventana.style.display = "none";
    });

    // Descargar gráfica (imagen)
    if (btnDescargarGrafica) {
        btnDescargarGrafica.addEventListener('click', () => {
            if (!chart) {
                alert('No hay gráfica para descargar.');
                return;
            }
            // Crear canvas temporal con fondo blanco
            const tempCanvas = document.createElement('canvas');
            const tempCtx = tempCanvas.getContext('2d');
            tempCanvas.width = canvas.width;
            tempCanvas.height = canvas.height;
            tempCtx.fillStyle = '#ffffff';
            tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
            tempCtx.drawImage(canvas, 0, 0);
            const link = document.createElement('a');
            const anio = (document.querySelector('.ventana-calendario select')?.value) || new Date().getFullYear();
            link.href = tempCanvas.toDataURL('image/png');
            link.download = `grafica_anual_${anio}.png`;
            link.click();

        });
    }

    // Descargar datos (Excel)
    if (btnDescargarDatos) {
        btnDescargarDatos.addEventListener('click', () => {
            // Obtener año seleccionado del select correcto
            let anio = null;
            // Buscar el select de año dentro de la ventana-calendario
            document.querySelectorAll('.ventana-calendario select').forEach(sel => {
                if (sel.options && sel.options.length > 0 && sel.options[0].textContent.length === 4) {
                    anio = sel.value;
                }
            });
            if (!anio) {
                anio = new Date().getFullYear().toString();
            }
            // Validar que el año sea string de 4 dígitos
            if (typeof anio !== 'string') anio = anio.toString();
            if (anio.length !== 4) {
                alert('Año inválido para la descarga.');
                return;
            }
            window.location.href = `/ingresos_egresos/descargar_informe_anual/?anio=${anio}`;

        });
    }
});