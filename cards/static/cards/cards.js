

$(document).ready( function() {

    var Field = {
        save: function(id, data, callback) {
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
                    var value = $('.field-name').val();
                    Field.save(id, {
                        name: value,
                    }, function() {
                        $('.selectable-field.active').text(value);
                    });
                });
                $('.field-alignment').change(function(e){
                    Field.save(id, {
                        alignment: e.target.value,
                    }, function() {
                        $('.selectable-field.active').css({
                            'textAlign': e.target.value,
                        });
                    });
                });
                $('#field-delete').click(function() {
                    Field.remove(id);
                });
            });
        },
        create: function() {
            $.ajax({
                url: '/field',
                type: 'PUT',
                success: function(response) {
                    $('.inner-card').append(response);
                    $('.inner-card .selectable-field').last().click(Field.click);
                }
            });
        },
        click: function() {
            $('.selectable-field.active').removeClass('active');
            $(this).addClass('active');
            $(this).draggable({
                axis:'y',
                containment: 'parent',
                stop: function(event, ui) {
                    Field.save(ui.helper.data('id'), {
                        top: ui.position.top / ui.helper.parent().height()
                    })
                },
            });
            Field.edit(this.dataset.id);
        },
        remove: function(id) {
            $.ajax({
                url: '/field/' + id,
                type: 'DELETE',
                success: function(response) {
                    window.location.reload();
                }
            });
        },
    };

    $('.selectable-field').click(Field.click);

    $('#add-field').click(function(){
        Field.create();
    });
});