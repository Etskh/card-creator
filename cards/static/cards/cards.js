

var createInputTimer = function( options ) {
    var timer = null;

    options.$elem.keyup( function() {
        if( timer ) {
            clearTimeout(timer);
        }
        timer = setTimeout(function(){

            timer = null;

            var value = options.$elem.val();
            if( options.regex ) {
                var $alert = $('.alert');
                if( !value.match(options.regex) ) {
                    $alert.find('.text').text(options.errorMessage);
                    $alert.show('blind');
                    return;
                }
                else {
                    $alert.hide('blind');
                }
            }

            options.success(value);
            options.$elem.addClass('success');
            setTimeout(function(){
                options.$elem.addClass('success');
            }, 500)
            console.log('Saved');
        }, 1000);
    });
}


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

                createInputTimer({
                    $elem: $('.field-name'),
                    regex: /^[a-zA-Z\-]+$/,
                    errorMessage: 'Name can only contain letters, numbers, and dashes',
                    success: function( value ) {
                        Field.save(id, {
                            name: value,
                        }, function() {
                            $('.selectable-field.active').text(value);
                        });
                    },
                });
                createInputTimer({
                    $elem: $('.field-template'),
                    success: function( value ) {
                        Field.save(id, {
                            template: value,
                        });
                    },
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
                $('.field-bold').click(function(e){
                    var $elem = $(e.currentTarget);
                    $elem.toggleClass('active');
                    var isBold = $elem.hasClass('active');
                    Field.save(id, {
                        is_bold: isBold,
                    }, function() {
                        $('.selectable-field.active').css({
                            'fontWeight': isBold ? 'bold' : 'normal',
                        });
                    });
                });
                $('.field-italic').click(function(e){
                    var $elem = $(e.currentTarget);
                    $elem.toggleClass('active');
                    var isItalic = $elem.hasClass('active');
                    console.log(isItalic);
                    Field.save(id, {
                        is_italic: isItalic,
                    }, function() {
                        $('.selectable-field.active').css({
                            'fontStyle': isItalic ? 'italic' : 'normal',
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
                    });
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
                },
            });
        },
    };

    $('.selectable-field').click(Field.click);

    $('#add-field').click(function(){
        Field.create();
    });
});