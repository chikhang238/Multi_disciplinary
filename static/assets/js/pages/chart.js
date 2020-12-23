var light = [];
var temp = [];
var light_dataset;
var temp_dataset;
var totalPoints = 40;
var updateInterval = 5000;
var now = new Date().getTime();

var options = {
         grid: {
          borderColor: '#f3f3f3',
          borderWidth: 1,
          tickColor: '#f3f3f3'
        },
        series: {
          color: '#3c8dbc',
          lines: {
            lineWidth: 2,
            show: true,
            fill: true,
          },
        },
        yaxis: {
          min: 0,
          max: 100,
          show: true
        },
        xaxis: {
           mode: "time",
        tickSize: [60, "second"],
        tickFormatter: function (v, axis) {
            var date = new Date(v);

            if (date.getSeconds() % 20 == 0) {
                var hours = date.getHours() < 10 ? "0" + date.getHours() : date.getHours();
                var minutes = date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes();
                var seconds = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();

                return hours + ":" + minutes + ":" + seconds;
            } else {
                return "";
            }
        },
        axisLabel: "Time",
        axisLabelUseCanvas: true,
        axisLabelFontSizePixels: 12,
        axisLabelFontFamily: 'Verdana, Arial',
        axisLabelPadding: 10
        }
};

function initData() {
    for (var i = 0; i < totalPoints; i++) {
        var tem = [now += updateInterval, 0];

        light.push(tem);
        temp.push(tem);
    }
}

// function GetData() {
//     $.ajaxSetup({ cache: false });

//     $.ajax({
//         url: "http://www.jqueryflottutorial.com/AjaxUpdateChart.aspx",
//         dataType: 'json',
//         success: update,
//         error: function () {
//             setTimeout(GetData, updateInterval);
//         }
//     });
// }

var tempLight;
var tempTemp;

function updateLight(_data) {
    light.shift();

    now += updateInterval

    tempLight = [now, _data['value']];
    light.push(tempLight);

    light_dataset = [
        { label: "Light:" + _data['value'] + "%", data: light, lines: { fill: true, lineWidth: 1.2 }, color: "#00FF00" }      
    ];

    $.plot($("#light_interactive"), light_dataset, options);
    // setTimeout(GetData, updateInterval);
}

function updateTemp(_data) {
    temp.shift();

    now += updateInterval;

    tempTemp = [now, _data['value']];
    temp.push(tempTemp);

    temp_dataset = [
        { label: "Temp:" + _data['value'] + "%", data: temp, lines: { fill: true, lineWidth: 1.2 }, color: "#00FF00" }      
    ];

    $.plot($("#temp_interactive"), temp_dataset, options);
    // setTimeout(GetData, updateInterval);
}

var room_id;


$(document).ready(function () {
    // setTimeout(GetData, updateInterval);
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    // var topic = "home/light";
    // var data1 = '{"topic": "' + topic + '"}';
    // socket.emit('subscribe', data=data1);
    $('#subscribe').click(function(event) {
        var topic = "LightSensor";
        var data = '{"topic": "' + topic + '"}';
        var topic1 = "TempSensor";
        var data1 = '{"topic": "' + topic1 + '"}';
        socket.emit('subscribe', data='{"topic": "LightSensor"}');
        socket.emit('subscribe', data='{"topic": "TempSensor"}');
        room_id = $( "#rooms" ).val();
        light = [];
        temp = [];
        initData();

        light_dataset = [        
            { label: "Light", data: light, lines:{fill:true, lineWidth:1.2}, color: "#00FF00" }
        ];

        temp_dataset = [        
            { label: "Temp", data: temp, lines:{fill:true, lineWidth:1.2}, color: "#00FF00" }
        ];

        $.plot($("#light_interactive"), light_dataset, options);
        $.plot($("#temp_interactive"), temp_dataset, options);
        // console.log(room_id);
    });
    socket.on('mqtt_message', function(data2) {
        console.log(data2['payload']['room']);
        if (data2['payload']['room'] == room_id) {
            if (data2['topic']=="LightSensor") updateLight(data2['payload']);
            else if (data2['topic']=="TempSensor") updateTemp(data2['payload']);
        }
        //     dat.push(parseInt(data2['payload']));
        //     console.log(dat);
        //     chartID = setInterval(function(){add_data(chart,data['payload'])},0);
        // }
        // else{
        //   add_data(chart1,data['payload']);
        //   chart1ID = setInterval(function(){add_data(chart1,data['payload'])},0);
        // }
    })
});