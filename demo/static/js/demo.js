$(function () {
    $('#submit').on('click', function () {
        if (jQuery.trim($('#word').val()).length > 0 && $(this).hasClass('btn-primary')) {
            $(this).removeClass('btn-primary').addClass('btn-danger');
            $(this).attr('value', 'Searching...')
        }
    });

    $("#model").change(function () {
        var value = $("#model option[]:selected").val();
        if (value == 'bt') {
            // $(this).parent().nextAll('.form-group').fadeOut(300, function(){ $(this).remove();});
            $(this).parent().nextAll('.form-group').collapse('hide');
        } else {
            $(this).parent().nextAll('.form-group').collapse('show');
        }
    });

});