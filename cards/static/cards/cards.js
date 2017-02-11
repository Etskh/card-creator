
var Field = {
    change: function(e) {
        console.log('changed field');
    }
}


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

        // TODO: Deselect all other fields
        // TODO: Add the border-green
        $(this).addClass('active');

        // select the field!
        $.get('/field/' + this.dataset.id, function(body) {
            $('#field-edit').html(body);
        });
    });
});

