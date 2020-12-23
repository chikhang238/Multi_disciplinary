
$(document).ready(function() {
     _getRooms();
});
    
function _getRooms() {
    $.get("/lookuprooms", function (data) {
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