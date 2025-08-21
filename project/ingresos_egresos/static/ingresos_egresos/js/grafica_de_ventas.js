// --- Descarga de Excel solo con los datos del gráfico mostrado ---
// Este script enlaza el botón "Descargar datos del gráfico (Excel)" con la vista exportar_ventas_grafico_excel,
// usando los valores actuales de mes y año seleccionados en el calendario.
document.addEventListener('DOMContentLoaded', function() {
    const btnDescargarGraficaExcel = document.getElementById('descargarGraficaExcel');
    if (btnDescargarGraficaExcel) {
        btnDescargarGraficaExcel.style.display = 'inline';
        let mes = (new Date().getMonth() + 1).toString();
        let anio = new Date().getFullYear().toString();
        document.addEventListener('click', function() {
            const selects = document.querySelectorAll('.ventana-calendario select');
            if (selects.length >= 2) {
                mes = selects[0].value;
                anio = selects[1].value;
            }
        });
        btnDescargarGraficaExcel.addEventListener('click', function(e) {
            e.preventDefault();
            const url = '/ingresos_egresos/ventas/exportar_grafico_excel/?mes=' + mes + '&anio=' + anio;
            window.location.href = url;
        });
    }
});
document.addEventListener("DOMContentLoaded", () => {
    console.log('⚡ grafica_de_ventas.js cargado');

    const canvas = document.getElementById("verVentas");
    const btnCalendario = document.getElementById("Calendario");
    const btnDescargar = document.getElementById('descargarBtn');
    let chart = null;

    // Elemento para mostrar el producto más vendido (si no existe, lo creamos)
    let masVendidoEl = document.getElementById('masVendido');
    if (!masVendidoEl) {
        masVendidoEl = document.createElement('p');
        masVendidoEl.id = 'masVendido';
        masVendidoEl.style.marginTop = '8px';
        const parent = canvas ? canvas.parentNode : document.body;
        parent.appendChild(masVendidoEl);
    }

    if (!canvas) {
        console.error("Falta el elemento canvas con id 'verVentas'.");
        alert("Error: No se encontró el canvas (id='verVentas').");
        return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('No se pudo obtener el contexto 2D del canvas.');
        alert('Error: No se pudo obtener el contexto 2D.');
        return;
    }

    if (typeof Chart === 'undefined') {
        console.error('Chart.js no está cargado.');
        alert('Error: Chart.js no está disponible. Incluye la librería antes de este script.');
        return;
    }

    function obtenerNombreMes(numeroMes) {
        const nombresMeses = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ];
        return nombresMeses[numeroMes - 1] || '';
    }

    function cargarGrafica(mes = (new Date().getMonth() + 1).toString(), anio = new Date().getFullYear().toString()) {
        // parseos y validaciones básicas
        mes = parseInt(mes, 10);
        anio = parseInt(anio, 10);
        if (!mes || isNaN(mes) || mes < 1 || mes > 12) {
            console.error('Mes inválido:', mes);
            alert('Por favor, seleccione un mes válido.');
            return;
        }
        if (!anio || isNaN(anio) || anio < 1900 || anio > new Date().getFullYear()) {
            console.error('Año inválido:', anio);
            alert('Por favor, seleccione un año válido.');
            return;
        }

        const nombreMes = obtenerNombreMes(mes);
        const url = `/ingresos_egresos/datos_informe_ventas/?mes=${mes}&anio=${anio}`; // Corrección: agregar prefijo ingresos_egresos/
        console.log(`Cargando gráfica de ventas para ${nombreMes} ${anio} — URL: ${url}`);

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    // intenta leer JSON de error si lo hay
                    return response.text().then(text => {
                        let parsed;
                        try { parsed = JSON.parse(text); } catch (e) { parsed = null; }
                        const errMsg = parsed && parsed.error ? parsed.error : `HTTP ${response.status}`;
                        throw new Error(errMsg);
                    });
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos recibidos del servidor (ventas):', data);

                // Validación: esperamos { labels: [...], ventas: [...], mas_vendido?: '...' }
                if (!data || !Array.isArray(data.labels) || !Array.isArray(data.ventas)) {
                    throw new Error('Formato inválido: se requiere {labels: [], ventas: []}. Recibido: ' + JSON.stringify(data));
                }

                if (data.labels.length !== data.ventas.length) {
                    console.warn('labels y ventas tienen longitudes distintas. Chart.js necesita mismas longitudes para etiquetado. Se seguirá intentando pero revisa backend.', {
                        labelsLen: data.labels.length,
                        ventasLen: data.ventas.length
                    });
                    // puedes optar por truncar o rellenar; aquí abortamos para evitar graficar mal:
                    throw new Error('labels y ventas deben tener la misma longitud.');
                }

                // destruir grafica previa si existe
                if (chart) {
                    chart.destroy();
                    chart = null;
                }

                // crear grafica
                chart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: data.labels,
                        datasets: [{
                            label: "Cantidad vendida",
                            data: data.ventas,
                            backgroundColor: "rgba(54, 162, 235, 0.5)",
                            borderColor: "rgba(54, 162, 235, 1)",
                            borderWidth: 1
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: `Ventas de ${nombreMes} ${anio} — Mejor producto: ${data.mas_vendido || "N/A"}`,
                                font: {
                                    size: 18  // Aumenta el tamaño de la fuente a 18 (puedes ajustarlo a 20, 24, etc.)
                                }
                            },
                            legend: { display: false },
                            tooltip: { enabled: true }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: "Cantidad" }
                            },
                            x: {
                                title: { display: true, text: "Productos" }
                            }
                        }
                    }
                });

                // mostrar mejor producto si viene
                masVendidoEl.textContent = `Producto más vendido: ${data.mas_vendido || 'No disponible'}`;
            })
            .catch(error => {
                console.error('Error al cargar datos de ventas:', error);
                alert('Error al cargar los datos de ventas: ' + (error.message || error));
            });
    }

    // cargar grafica inicial para mes actual
    cargarGrafica();

    const ventana = document.createElement('div');
    ventana.className = 'ventana-calendario';
    ventana.style.display = 'none';

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
    selectMes.value = new Date().getMonth() + 1;

    const labelAnio = document.createElement('label');
    labelAnio.textContent = 'Selecciona un año:';

    const selectAnio = document.createElement('select');
    const currentYear = new Date().getFullYear();
    for (let year = currentYear; year >= currentYear - 4; year--) {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        selectAnio.appendChild(option);
    }
    selectAnio.value = currentYear;

    const btnVer = document.createElement('button');
    btnVer.textContent = 'Ver';

    const btnCerrar = document.createElement('button');
    btnCerrar.textContent = 'Cerrar';

    const botonesContenedor = document.createElement('div');
    botonesContenedor.className = 'botones-contenedor';
    botonesContenedor.style.display = 'flex';
    botonesContenedor.style.justifyContent = 'center';
    botonesContenedor.style.gap = '100px';
    botonesContenedor.appendChild(btnVer);
    botonesContenedor.appendChild(btnCerrar);

    ventana.appendChild(labelMes);
    ventana.appendChild(selectMes);
    ventana.appendChild(labelAnio);
    ventana.appendChild(selectAnio);
    ventana.appendChild(botonesContenedor);
    document.body.appendChild(ventana);

    function posicionarVentana() {
        const rect = btnCalendario.getBoundingClientRect();
        const ventanaWidth = ventana.offsetWidth || 300;
        const ventanaHeight = ventana.offsetHeight || 300;

        const initialTop = rect.bottom + window.scrollY + 10;
        const initialLeft = rect.left + window.scrollX + (rect.width - ventanaWidth) / 2;

        ventana.style.top = initialTop + 'px';
        ventana.style.left = initialLeft + 'px';
        ventana.style.minWidth = '300px';
        ventana.style.transition = 'all 0.3s ease';

        setTimeout(() => {
            ventana.style.top = '50%';
            ventana.style.left = '50%';
            ventana.style.transform = 'translate(-50%, -50%)';
        }, 10);
    }

    btnCalendario.addEventListener('click', function (e) {
        e.stopPropagation();
        posicionarVentana();
        ventana.style.display = ventana.style.display === 'block' ? 'none' : 'block';
    });

    btnVer.addEventListener('click', function () {
        const mes = selectMes.value;
        const anio = selectAnio.value;
        cargarGrafica(mes, anio);
        ventana.style.display = 'none';
    });

    btnCerrar.addEventListener('click', function () {
        ventana.style.display = 'none';
    });

    // Menú de descarga: gráfica (imagen) y datos (Excel)
        const btnDescargarGrafica = document.getElementById('descargarGrafica');
        const btnDescargarDatos = document.getElementById('descargarDatos');
        const submenuDescarga = document.getElementById('submenuDescargaVentas');

        if (btnDescargarGrafica) {
            btnDescargarGrafica.addEventListener('click', (e) => {
                e.preventDefault();
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
                // Descargar imagen
                const link = document.createElement('a');
                const mes = selectMes.value || new Date().getMonth() + 1;
                const anio = selectAnio.value || new Date().getFullYear();
                link.href = tempCanvas.toDataURL('image/png');
                link.download = `grafica_ventas_${mes}_${anio}.png`;
                link.click();
            });
        }

        // Descargar datos del gráfico (Excel) usando la vista exportar_ventas_grafico_excel
        if (btnDescargarDatos) {
            btnDescargarDatos.addEventListener('click', function(e) {
                e.preventDefault();
                // Obtener mes y año seleccionados
                let mes = selectMes.value || (new Date().getMonth() + 1);
                let anio = selectAnio.value || new Date().getFullYear();
                // Construir la URL CORRECTA
                const url = `/ingresos_egresos/ventas/exportar_grafico_excel/?mes=${mes}&anio=${anio}`;
                window.location.href = url;
            });
        }
});
