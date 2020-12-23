var myElem = document.getElementById('search');
myElem.onclick = function() {
    var room_id = $( "#rooms" ).val();
    
	$.post("/get_result", {room_id: room_id}, function (data) {
        if (data != null && data != undefined && data.length) {
            var html = '';
            // html += '<option value="">--Không chọn--</option>';
            html += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css">';
            // html += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>';
            // html += ' <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js"></script>';
            // html += '<link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">';
            // html += '<link href= "https://cdn.jsdelivr.net/gh/gitbrent/bootstrap-switch-button@1.1.0/css/bootstrap-switch-button.min.css"rel="stylesheet" /> ';
            // html += '<link rel="stylesheet" type="text/css" href=  "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" />';
            html += '<link href="https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/css/bootstrap4-toggle.min.css" rel="stylesheet">';
            html += '<script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>';
            html += ' <script>$("input.switch").bootstrapSwitch();</script>';
            html += '<div class="col-xl-12"><div class="card"><div class="card-header"></div><div class="card-block table-border-style"><div class="table-responsive"><table class="table"><thead><tr><th>Device ID</th><th>Device Name</th><th>Status</th><th>Floor</th><th>Room</th></tr></thead><tbody>';
            //html += '<script>.slider:after {position: absolute;content: "OFF";top: 6px;right: 5px;color: #fff;font-size: 0.9em;}input:checked + .slider:after {content: "ON";left: 10px}</script>';
              
            $.each(data, function (index, value) {
                // html += '<option value=' + value + '>' + value + '</option>';
                html += '<tr><th scope="row">' + value['device_id'] + '</th><td>' + value['device_name'] + '</td><td>'
                
                if (value['status'] == 1) {
                    
                    html += '<input type="checkbox"   checked   class="switchbutton" value="On" />';
                   
                } else {
                html += '<input type="checkbox" class="switchbutton" value="On"   />';
                }

                
                html += '</td><td>' + value['floor'] + '</td><td>' + value['room_id'] + '</td></tr>';  
            });
            
            html += '</tbody></table></div></div></div></div>';
            $("#devices").html(html);
        }
        else $("#devices").html('No data');
    });
}



                                            // <tr>
                                            //     <th scope="row">1</th>
                                            //     <td>Mark</td>
                                            //     <td>Otto</td>
                                            //     <td>@mdo</td>
                                            // </tr>
                                            // <tr>
                                            //     <th scope="row">2</th>
                                            //     <td>Jacob</td>
                                            //     <td>Thornton</td>
                                            //     <td>@fat</td>
                                            // </tr>
                                            // <tr>
                                            //     <th scope="row">3</th>
                                            //     <td>Larry</td>
                                            //     <td>the Bird</td>
                                            //     <td>@twitter</td>
                                            // </tr>