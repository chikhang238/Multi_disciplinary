
$(document).ready(function() {
    $("#period").on('change', function () {
        var period = $(this).val();
        var date = $("#date").val();
        if (period != undefined && period != '' && date != undefined && date != '') {
            _getRooms(date, period);
        }
    });
    $("#date").on('change', function () {
        var period = $("#period").val();
        var date = $(this).val();
        if (period != undefined && period != '' && date != undefined && date != '') {
            _getRooms(date, period);
        }
    });
});
   
function _getRooms(date, period) {
   $.post("/bookroom", {date: date, period: period}) 
    .done(function (data) {
       if (data != null && data != undefined && data.length) {
           var html = '';
           // html += '<option value="">--Không chọn--</option>';
           $.each(data, function (index, value) {
               html += '<option value=' + value + '>' + value + '</option>';
           });
           $("#rooms").html(html);
       }
   });
}