// Obtener los datos del contexto de Django
var nombresPaquetes = JSON.parse(document.getElementById('nombresPaquetes').textContent);
var cantidadReservas = JSON.parse(document.getElementById('cantidadReservas').textContent);

// Inicializar el gráfico
var chart = echarts.init(document.getElementById('reservasGrafico'));

// Opciones de configuración para el gráfico de barras
var options = {
    title: {
        text: 'Número de Reservas por Paquete Turístico'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    grid: {
        bottom: 260  // Aumentar el margen inferior para que los nombres tengan más espacio
    },
    xAxis: {
        type: 'category',
        data: nombresPaquetes,
        name: 'Paquetes Turísticos',
        axisLabel: {
            rotate: 44, // Rotar para mostrar mejor los nombres largos
            fontSize: 12,  // Ajustar tamaño de la fuente para nombres largos
            interval: 0,  // Mostrar todos los nombres
        }
    },
    yAxis: {
        type: 'value',
        name: 'Número de Reservas'
    },
    series: [{
        data: cantidadReservas,
        type: 'bar',
        barWidth: '50%',
        itemStyle: {
            color: '#5470C6'
        },
        label: {
            show: true,  // Mostrar los números sobre las barras
            position: 'top',
            formatter: '{c}'
        }
    }]
};

// Renderizar el gráfico con las opciones configuradas
chart.setOption(options);
