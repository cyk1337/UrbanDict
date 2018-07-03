$(function () {
    $('#submit').on('click', function () {
        if (jQuery.trim($('#word').val()).length > 0 && $(this).hasClass('btn-primary')){
            $(this).removeClass('btn-primary').addClass('btn-danger');
            $(this).attr('value', 'Searching...')
        }
    })
})