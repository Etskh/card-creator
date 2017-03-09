

var createInputTimer = function( options ) {
    var timer = null;
    var callback = function() {
        var target = this;
        if( timer ) {
            clearTimeout(timer);
        }
        timer = setTimeout(function(){

            timer = null;

            var value = $(target).val();
            if( options.regex ) {
                var $alert = options.$errorElem;
                if( !value.match(options.regex) ) {
                    $alert.find('.text').text(options.errorMessage);
                    $alert.show('blind');
                    if( options.error ) {
                        options.error();
                    }
                    return;
                }
                else {
                    $alert.hide('blind');
                }
            }

            if( options.success ) {
                options.success(value, $(target));
            }
            $(target).addClass('success');
            setTimeout(function(){
                $(target).addClass('success');
            }, 500)
            console.log(`Saved: {target.id()}`);
        }, 1000);
    } // callback()


    if( options.$elem.attr('type') == 'number' ) {
        options.$elem.change(callback);
    }
    else {
        options.$elem.keyup(callback);
    }
}


var CardData = {
    init: function() {
        createInputTimer({
            $elem: $('.datatype-name'),
            regex: /^[a-zA-Z\-]+$/,
            $errorElem: $('#cardtype-alert'),
            errorMessage: 'Name can only contain letters, and dashes',
            success: function( value, $element ) {
                var id = $element.data('id');
                CardData.save(id, {
                    name: value,
                }, function() {
                    // empty
                });
            },
        });
    },
    create: function(callback) {
        $.ajax({
            url: '/data',
            type: 'PUT',
            success: function(response) {
                $('#data-list').append(response);
                CardData.init();
            }
        });
    },
    save: function(id, data, callback) {
        $.post('/data/' + id, data, function(response){
            if( callback ) {
                callback();
            }
        });
    },
};


var CardType = {
    save: function(id, data, callback) {
        $.post('/cardtype/' + id, data, function(response){
            if( callback ) {
                callback();
            }
        });
    },
};

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
                $errorElem: $('#field-alert'),
                errorMessage: 'Name can only contain letters, and dashes',
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
            $('.choose-font').click(function(){
                var fontId = $(this).data('id');
                var fontCss = $(this).css('fontFamily');
                var fontName = $(this).text();

                Field.save(id, {
                    font_id: fontId,
                }, function() {
                    $('#font-select').text(fontName)
                    $('#font-select').css({
                        'fontFamily': fontCss
                    });
                    $('.selectable-field.active').css({
                        'fontFamily': fontCss
                    });
                });
            });
            createInputTimer({
                $elem: $('#font-size'),
                success: function( value ) {
                    console.log('asdf');
                    var size = parseInt(value);
                    Field.save(id, {
                        font_size: size,
                    }, function() {
                        $('.selectable-field.active').css({
                            'fontSize': size + '%',
                        });
                    });
                },
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



var Card = {
    create: function(cardType, name, callback) {
        /*$.get('/type/'+ cardType +'/new-card', {}, function(response) {
            $('#card-edit-modal .modal-title').text('New Card');
            $('#card-edit-modal .modal-body').html(response);
            $('#card-edit-modal').modal('show');
        });*/
    },
    createNew: function() {
        console.log()
    },
    open: function(id, callback) {
        $.get('/card/' + id, {}, function(response) {
            $('#card-edit-modal .modal-body').html(response);
            createInputTimer({
                $elem: $('#card-name'),
                regex: /^[a-zA-Z\- ]+$/,
                $errorElem: $('#carddata-alert'),
                errorMessage: 'Name can only contain letters, dashes, and spaces',
            });
            createInputTimer({
                $elem: $('#card-count'),
                regex: /^[0-9]+$/,
                $errorElem: $('#carddata-alert'),
                errorMessage: 'Card count needs to be a number',
            });
            $('#card-edit-modal').modal('show');
        });
    },
    saveOpen: function() {
        var id = $('#card-id').val();
        var name = $('#card-name').val();
        var count = $('#card-count').val();

        var $cardData = $('.card-data-value');
        var data = {};
        for( var d=0; d<$cardData.length; d++) {
            console.log($cardData[d]);
            data[$cardData[d].dataset.name] = $cardData[d].value;
        }

        Card.save(id, {
            title: name,
            count: count,
            data: data,
        }, function() {
            // update the row
            var $row = $('#card-'+id);
            $row.find('td.title').text(name);
            $row.find('td.count').text(count);
            for( var name in data ) {
                $row.find('td.data-'+name).text(data[name]);
            }
            // close the modal
            $('#card-edit-modal').modal('hide');
        });
    },
    save: function(id, data, callback) {
        console.log(data);
        $.post('/card/' + id, data, function(response){
            if( callback ) {
                callback();
            }
        });
    },
    init: function() {
        $('#add-card').click(function(){
            $('#card-new-modal').modal('show');
        });
        $('button#card-new').click(function() {
            var $name = $('#new-card-name');
            Card.create( $name.data('cardTypeId'), $name.val(), function() {
                $('#card-new-modal').modal('hide');
            });
        });
        createInputTimer({
            $elem: $('#new-card-name'),
            regex: /^[a-zA-Z\- ]+$/,
            $errorElem: $('#new-carddata-alert'),
            errorMessage: 'Name can only contain letters, dashes, and spaces',
            success: function(){
                $('button#card-new').prop('disabled', false);
            },
            error: function() {
                $('button#card-new').prop('disabled', true);
            },
        });
        $('.card-row').click(function() {
            var target = this;
            var id = $(this).data('id');
            var name = $(this).data('name');
            $('#card-edit-modal .modal-title').text(name);
            Card.open(id);
        });
        $('#card-save').click(Card.saveOpen);
    },
};


$(document).ready( function() {

    //
    // Card type editing
    //
    $('.selectable-field').click(Field.click);

    $('#add-field').click(function(){
        Field.create();
    });

    $('#add-data').click(function(){
        CardData.create();
    });
    CardData.init();

    createInputTimer({
        $elem: $('.cardtype-name'),
        regex: /^[a-zA-Z\-]+$/,
        $errorElem: $('#cardtype-alert'),
        errorMessage: 'Name can only contain letters, and dashes',
        success: function( value ) {
            $('#cardtype-name-label').addClass('label-success');
            setTimeout(function() {
                $('#cardtype-name-label').removeClass('label-success');
            }, 1000);
            var id = $('.cardtype-name').data('id');
            CardType.save(id, {
                name: value,
            }, function() {
                // empty
            });
        },
    });


    // Card data editing
    //
    Card.init();
});