$(document).ready(function () {
    /*
     * Flot Interactive Chart
     * -----------------------
     */
    // We use an inline data source in the example, usually data would
    // be fetched from a server
    var light = [];
    var dataset;
    var totalPoints = 100;
    var updateInterval = 1000;
    var now = new Date().getTime();
    
    function initData() {
        for (var i = 0; i < totalPoints; i++) {
            var temp = [now += updateInterval, 0];
    
            light.push(temp);
        }
    }

    var temp;
 
    function update(_data) {
        //remove first item of array
        light.shift();
    
        now += updateInterval
    
        //add the data retrieve from backend to array
        temp = [now, _data['payload']];
        light.push(temp);
    
        //update legend label so users can see the latest value in the legend
        dataset = [
            { label: "Light:" + _data['payload'] + "%", data: light, lines: { fill: true, lineWidth: 1.2 }, color: "#00FF00" }      
        ];
    
        //redraw the chart
        $.plot($("#interactive"), dataset, options);
    
        //prepare for next update
        // setTimeout(GetData, updateInterval);
    }

    // var dat       = [10,20,30,20,50,60,70,10,50,30],
    //     totalPoints = 100
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var topic = "home/light";
    var data1 = '{"topic": "' + topic + '"}';
    socket.emit('subscribe', data=data1);
    socket.on('mqtt_message', function(data2) {
        update(data2);
        // if (data2['topic']=="home/light"){
        //     dat.push(parseInt(data2['payload']));
        //     console.log(dat);
        //     chartID = setInterval(function(){add_data(chart,data['payload'])},0);
        // }
        // else{
        //   add_data(chart1,data['payload']);
        //   chart1ID = setInterval(function(){add_data(chart1,data['payload'])},0);
        // }
    })

    // function getRandomData() {

    //   if (dat.length > 0) {
    //     dat = dat.slice(1)
    //   }

      // Do a random walk
    //   while (data.length < totalPoints) {

    //     var prev = data.length > 0 ? data[data.length - 1] : 50,
    //         y    = prev + Math.random() * 10 - 5

    //     if (y < 0) {
    //       y = 0
    //     } else if (y > 100) {
    //       y = 100
    //     }

    //     data.push(y)
    //   }

      // Zip the generated y values with the x values
    //   var res = []
    //   for (var i = 0; i < dat.length; ++i) {
    //     res.push([i, dat[i]])
    //   }

    //   return res
    // }

    // var interactive_plot = $.plot('#interactive', [
    //     {
    //       data: getRandomData(),
    //     }
    //   ],
    //   {
    //     grid: {
    //       borderColor: '#f3f3f3',
    //       borderWidth: 1,
    //       tickColor: '#f3f3f3'
    //     },
    //     series: {
    //       color: '#3c8dbc',
    //       lines: {
    //         lineWidth: 2,
    //         show: true,
    //         fill: true,
    //       },
    //     },
    //     yaxis: {
    //       min: 0,
    //       max: 100,
    //       show: true
    //     },
    //     xaxis: {
    //       show: true
    //     }
    //   }
    // )

    // var updateInterval = 500 //Fetch data ever x milliseconds
    // var realtime       = 'on' //If == to on then fetch data every x seconds. else stop fetching
    // function update() {

    //   interactive_plot.setData([getRandomData()])

    //   // Since the axes don't change, we don't need to call plot.setupGrid()
    //   interactive_plot.draw()
    //   if (realtime === 'on') {
    //     setTimeout(update, updateInterval)
    //   }
    // }

    // //INITIALIZE REALTIME DATA FETCHING
    // if (realtime === 'on') {
    //   update()
    // }
    // //REALTIME TOGGLE
    // $('#realtime .btn').click(function () {
    //   if ($(this).data('toggle') === 'on') {
    //     realtime = 'on'
    //   }
    //   else {
    //     realtime = 'off'
    //   }
    //   update()
    // })
})