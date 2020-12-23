$(document).ready(function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var chartID = 0;
    var chart1ID = 0;
    Chart.defaults.global.defaultFontColor='white';


    $('#publish').click(function(event) {
      var topic = $('#topic').val();
      if (topic == "home/light"){
        if (chartID != 0){
          clearInterval(chartID);
        }
      }
      else{
        if (chart1ID != 0){
          clearInterval(chart1ID);
        }
      }
      var message = $('#message').val();
      var qos = $('#qos').val();
      var data = '{"topic": "' + topic + '", "message": "' + message + '", "qos": ' + qos + '}';
      socket.emit('publish', data=data);
    });

    $('#subscribe').click(function(event) {
      var topic = "home/light";
      var data = '{"topic": "' + topic + '"}';
      socket.emit('subscribe', data=data);
      $('#subscribe').hide();
      $('#unsubscribe').show();
      $('#subscribe_topic').prop('readonly', true);
    });

    $('#subscribe1').click(function(event) {
      var topic = "home/temp";
      var data = '{"topic": "' + topic + '"}';
      socket.emit('subscribe', data=data);
      $('#subscribe1').hide();
      $('#unsubscribe1').show();
      $('#subscribe_topic').prop('readonly', true);
    });


    $('#unsubscribe').click(function(event) {
      if (chartID != 0){
        clearInterval(chartID);
      }
      var topic = "home/light";
      var data = '{"topic": "' + topic + '"}';
      socket.emit('unsubscribe', data=data);
      $('#subscribe').show();
      $('#unsubscribe').hide();
      $('#subscribe_topic').prop('readonly', false);
    });

    $('#unsubscribe1').click(function(event) {
      if (chart1ID != 0){
        clearInterval(chart1ID);
      }
      var topic = "home/temp";
      var data = '{"topic": "' + topic + '"}';
      socket.emit('unsubscribe', data=data);
      $('#subscribe1').show();
      $('#unsubscribe1').hide();
      $('#subscribe_topic').prop('readonly', false);
    });

    socket.on('mqtt_message', function(data) {
      if (data['topic']=="home/light"){
        add_data(chart,data['payload']);
        chartID = setInterval(function(){add_data(chart,data['payload'])},0);
      }
      else{
        add_data(chart1,data['payload']);
        chart1ID = setInterval(function(){add_data(chart1,data['payload'])},0);
      }
    })

    function add_data(topicChart,value){
        label = new Date();
        topicChart.data.labels.push(label);
        topicChart.data.datasets.forEach((dataset) => {
          dataset.data.push(value);
        });
        topicChart.update();
    };
    

    var ctx = document.getElementById('myChart').getContext('2d');
    var chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [{
            label: 'Home/Light Sensor',
            backgroundColor: 'rgb(121,198,255)',
            borderColor: 'rgb(121,198,255)',
            data: [],
        }]
    },
    options: {
      responsive: true,
      scales: {
        yAxes: [{
          ticks: {
            max: 100,
            min: 0,
            stepSize: 10,
            fontSize: 14,
            gridLines: {
              display: false,
              color: "#000000",
              lineWidth: 1,
            }  
          },
          gridLines: {
            display: false,
            color: "#000000",
            lineWidth: 3,
          }
        }],
        xAxes: [{
          type: 'time',
          time: {
            unit: 'second'
          },
          gridLines: {
            display: false,
            color: "#000000",
            lineWidth: 3,
          },
          
        }]
      }
    }
    });

    var ctx1 = document.getElementById('myChart1').getContext('2d');

    var chart1 = new Chart(ctx1, { 
    type: 'line',
    data: {
        datasets: [{
            label: 'Home/Temp Sensor',
            backgroundColor: 'rgb(255,167,250)',
            borderColor: 'rgb(255,167,250)',
            data: [],
            steppedLine: true,
        }]
    },
    options: {
      responsive: true,
      scales: {
        yAxes: [{
          ticks: {
            max: 100,
            min: 0,
            stepSize: 10,
            fontSize: 14,
            display: false,
          },
          gridLines: {
            display: false,
            color: "#000000",
            lineWidth: 3,
          }
        }],
        xAxes: [{
          type: 'time',
          time: {
            unit: 'second'
          },
          gridLines: {
            display: false,
            color: "#000000",
            lineWidth: 3,
          }          
        }]
      }
    }
    });


});