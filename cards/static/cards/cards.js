

$(document).ready( function() {

    var Field = {
        save: function(id, data, callback) {
            console.log('saving field ' + id + 'now...');
            console.log(data);
            $.post('/field/' + id, data, function(response){
                if( callback ) {
                    callback();
                }
            });
        },
        edit: function(id) {
            // Show the edit widgets
            $.get('/field/' + id, function(body) {
                $('#field-edit').html(body);
                $('.field-name').keyup( function() {
                    console.log(arguments);
                    var value = $('.field-name').val();
                    Field.save(id, {
                        name: value,
                    }, function() {
                        $('.selectable-field.active').text(value);
                    });
                });
            });
        }
    };

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
        $('.selectable-field.active').removeClass('active');
        $(this).addClass('active');
        $(this).draggable({
            axis:'y',
            containment: 'parent',
            cursor: "crosshair",
            stop: function(event, ui) {
                Field.save(ui.helper.data('id'), {
                    top: ui.position.top / ui.helper.parent().height()
                })
            },
        });
        Field.edit(this.dataset.id);
    });
});