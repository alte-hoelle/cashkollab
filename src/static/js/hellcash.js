

function get_data_and_write_to_element_id(url, element_id = "output") {
    $.ajax({
        url: url,
        success: function (data) {
            document.getElementById('element_id').innerHTML = data;
        }

    });
}


setTimeout(function () {
    if ($('#msg').length > 0) {
        $('#msg').remove();
    }
}, 2000)

$(document).ready(function() {
    $(".dropdown-toggle").dropdown();
});

