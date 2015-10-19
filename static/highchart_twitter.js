$(function () {
$('#botonHighchart').click(

    function(){

    $('#container').highcharts({


        <%
            palabra = base_datos[0]["palabra"]
            rt_medio = base_datos[0]["rt_medio"]
        %>

        chart: {
                type: 'column'
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
            yAxis: 0,
            name: ${palabra},
            data: [${rt_medio}]

        }]
    });
 
});
});
