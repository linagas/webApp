console.log('js')
var dataUf =$( "#chartdiv" ).data( "lastValue" );
var dataDolar =$( "#dolardiv" ).data( "dolarValue" );

for (var prop in dataUf) {
    dataUf[prop].Valor = parseFloat(dataUf[prop].Valor);
}
var chart = AmCharts.makeChart( "chartdiv", {
    "type": "serial",
    "theme": "light",
    "titles": [{
        "text": "Graficas UF."
      }],
    "dataProvider": dataUf,
    "valueAxes": [ {
      "gridColor": "#FFFFFF",
      "gridAlpha": 0.2,
      "dashLength": 0
    } ],
    "gridAboveGraphs": true,
    "startDuration": 1,
    "graphs": [ {
      "balloonText": "[[category]]: <b>[[value]]</b>",
      "fillAlphas": 0.8,
      "lineAlpha": 0.2,
      "type": "column",
      "valueField": "Valor"
    } ],
    "chartCursor": {
      "categoryBalloonEnabled": false,
      "cursorAlpha": 0,
      "zoomable": false
    },
    "categoryField": "Fecha",
    "categoryAxis": {
      "gridPosition": "start",
      "gridAlpha": 0,
      "tickPosition": "start",
      "tickLength": 20
    },
    "export": {
      "enabled": true
    }
  
  } );
  console.log('----------------USD-----------------------',dataDolar);
  for (var prop in dataDolar) {
    if(dataDolar.length > 0){
        if(dataDolar[prop].Fecha != "No Disponible"){
            dataDolar[prop].Valor = parseFloat(dataDolar[prop].Valor);
        }else{
            dataDolar[prop].Valor = 0;
            dataDolar[prop].Fecha = ''
        }
    }
}
  var chart2 = AmCharts.makeChart( "dolardiv", {
    "type": "serial",
    "theme": "light",
    "titles": [{
        "text": "Graficas Dolar."
      }],
    "dataProvider": dataDolar,
    "valueAxes": [ {  "gridColor": "#FFFFFF",
      "gridAlpha": 0.2,
      "dashLength": 0
    } ],
    "gridAboveGraphs": true,
    "startDuration": 1,
    "graphs": [ {
      "balloonText": "[[category]]: <b>[[value]]</b>",
      "fillAlphas": 0.8,
      "lineAlpha": 0.2,
      "type": "column",
      "valueField": "Valor"
    } ],
    "chartCursor": {
      "categoryBalloonEnabled": false,
      "cursorAlpha": 0,
      "zoomable": false
    },
    "categoryField": "Fecha",
    "categoryAxis": {
      "gridPosition": "start",
      "gridAlpha": 0,
      "tickPosition": "start",
      "tickLength": 20
    },
    "export": {
      "enabled": true
    }
  
  } );

chart.write ("chartdiv");
chart2.write ("chart2div");
    