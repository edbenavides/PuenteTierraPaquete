// static/js/clientes_pais_grafico.js

document.addEventListener('DOMContentLoaded', function() {
    var chartDom = document.getElementById('graficoClientesPaisMes');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        tooltip: {
            trigger: 'item'
        },
        legend: {
            top: '2%',
            left: 'center',
        },
        series: [
            {
                name: 'Clientes',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 8, // Esquinas redondeadas
                    borderColor: '#fff',
                    borderWidth: 3
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '30',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: chartData  // Insertar los datos de la gráfica
            }
        ]
    };

    option && myChart.setOption(option);
});
