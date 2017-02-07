

$(document).ready( function() {

    // Do init stuff here
    $('#done-editing').click(function() {
        // go back to the main page
        window.location.href = '/';
    });
    $('#start-editing').click(function() {
        // go back to the main page
        window.location.href = '/edit';
    });

    $('.selectable-field').click(function() {
        // select the field!
        $('#field-edit').html('This is the new field');
    });
});

