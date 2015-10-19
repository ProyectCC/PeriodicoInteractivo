$(function () {
$('button').click(

    function(){

    $('#container').highcharts({

        data: {
            table: document.getElementById('datatable')
        },
        chart: {
                type: document.getElementById('tipoGrafica').value
        },
        title: {
            text: 'Edad de los usuarios'
        },
        yAxis: [{
            allowDecimals: false,
            title: {
                text: 'Número de usuarios'
            }
        }],
        tooltip: {
            formatter: function() {
                return '<b>'+ this.series.name +'</b><br/>'+
                    this.point.y +' '+ this.point.name.toLowerCase();
            }
        },
        series: [{
            yAxis: 0
        }]
    });
 
});
});
