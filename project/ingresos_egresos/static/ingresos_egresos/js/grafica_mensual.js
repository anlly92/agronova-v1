document.addEventListener('DOMContentLoaded', function () {
    console.log('⚡ grafica_mensual.js cargado');

    const canvas = document.getElementById('verMensual');
    const btnCalendario = document.getElementById('Calendario');
    const btnDescargar = document.getElementById('descargarBtn');
    let chart;

    // Verificar que los elementos existan
    if (!canvas) {
        console.error("Falta el elemento canvas con id 'verMensual'.");
        alert("Error: No se encontró el canvas.");
        return;
    }

    if (!btnCalendario) {
        console.error("Falta el botón con id 'Calendario'.");
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
        alert('Error: Chart.js no está disponible.');
        return;
    }

    function cargarGrafica(mes = (new Date().getMonth() + 1).toString(), anio = new Date().getFullYear().toString()) {
        console.log(`Cargando gráfica para mes: ${mes}, año: ${anio}`);

        // Validación de mes y año
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

        const url = `/ingresos_egresos/datos_informe_mensual/?mes=${mes}&anio=${anio}`;
        console.log('Enviando solicitud a:', url);

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
                console.log('Datos recibidos del servidor:', data);
                if (!data.labels || !data.data || !data.data.ingresos || !data.data.egresos) {
                    throw new Error('Datos incompletos en la respuesta: ' + JSON.stringify(data));
                }

                if (chart) chart.destroy();

                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: `Ingresos ${mes}/${anio}`,
                                data: data.data.ingresos,
                                backgroundColor: '#2e7d32', // Verde oscuro, igual que anual
                                borderColor: '#1b5e20',
                                borderWidth: 1
                            },
                            {
                                label: `Egresos ${mes}/${anio}`,
                                data: data.data.egresos,
                                backgroundColor: '#c62828', // Rojo oscuro, igual que anual
                                borderColor: '#8e0000',
                                borderWidth: 1
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Monto'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Día'
                                }
                            }
                        }
                    }
                });

                if (data.warning) {
                    console.warn('Advertencia del servidor:', data.warning);
                    alert(data.warning);
                }
            })
            .catch(error => {
                console.error('Error en fetch:', error);
                alert('Error al cargar los datos de la gráfica: ' + error.message);
            });
    }

    // Cargar gráfica inicial con el mes y año actuales
    console.log('Cargando gráfica inicial para mes:', new Date().getMonth() + 1, 'año:', new Date().getFullYear());
    cargarGrafica();

    // Crear ventana emergente
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

    // Contenedor para los botones
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

    // Posicionar ventana debajo del ícono Calendario y luego centrar
    function posicionarVentana() {
        const rect = btnCalendario.getBoundingClientRect();
        const ventanaWidth = ventana.offsetWidth || 300;
        const ventanaHeight = ventana.offsetHeight || 300;

        // Posición inicial justo debajo del ícono Calendario
        const initialTop = rect.bottom + window.scrollY + 10;
        const initialLeft = rect.left + window.scrollX + (rect.width - ventanaWidth) / 2;

        ventana.style.top = initialTop + 'px';
        ventana.style.left = initialLeft + 'px';
        ventana.style.minWidth = '300px';
        ventana.style.transition = 'all 0.3s ease';

        // Después de un breve delay, centra la ventana
        setTimeout(() => {
            ventana.style.top = '50%';
            ventana.style.left = '50%';
            ventana.style.transform = 'translate(-50%, -50%)';
        }, 10);
    }

    // Mostrar u ocultar ventana con #Calendario
    btnCalendario.addEventListener('click', function (e) {
        e.stopPropagation();
        posicionarVentana();
        ventana.style.display = ventana.style.display === 'block' ? 'none' : 'block';
    });

    // Actualizar gráfica con el mes y año seleccionados
    btnVer.addEventListener('click', function () {
        const mes = selectMes.value;
        const anio = selectAnio.value;
        cargarGrafica(mes, anio);
        ventana.style.display = 'none';
    });

    // Cerrar ventana
    btnCerrar.addEventListener('click', function () {
        ventana.style.display = 'none';
    });

    // Soporte para el botón #descargarBtn
if (btnDescargar) {
    btnDescargar.addEventListener('click', () => {
        if (!chart) {
            alert('No hay gráfica para descargar.');
            return;
        }

        // Crear canvas temporal con fondo blanco
        const tempCanvas = document.createElement('canvas');
        const tempCtx = tempCanvas.getContext('2d');
        tempCanvas.width = canvas.width;
        tempCanvas.height = canvas.height;

        // Fondo blanco
        tempCtx.fillStyle = '#ffffff';
        tempCtx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);

        // Copiar gráfico encima
        tempCtx.drawImage(canvas, 0, 0);

        // Descargar imagen
        const link = document.createElement('a');
        link.href = tempCanvas.toDataURL('image/png');
        const mes = selectMes.value || new Date().getMonth() + 1;
        const anio = selectAnio.value || new Date().getFullYear();
        link.download = `grafica_mensual_${mes}_${anio}.png`;
        link.click();
    });
    console.log('Evento click asignado al botón descargarBtn');
}
});