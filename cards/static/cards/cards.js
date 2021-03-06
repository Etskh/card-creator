
var core = {

    /**
     creates a wrapper around an input to
     validate on change, and send a callback
     {
        @param {string|regex} regex: a pattern to match against, or a special string
            'email'
        @param {object} $elem: the jquery object of the input to wrap
        @param {object} $errorElem: the jquery object to display errors
        @param {string} errorMessage: an explanation of the correct entry format
        @param {function} success: callback upon success
     }
    */
    createInputTimer: function( options ) {
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

                    if (options.regex == 'email') {
                        options.regex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
                    }

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
                }, 500);

            }, 1000);
        } // callback()


        if( options.$elem.attr('type') == 'number' ) {
            options.$elem.change(callback);
        }
        else {
            options.$elem.keyup(callback);
        }
    }, // createInputTimer


    /**
      create a RESTful object around a model and a configuration
      @param model {string} name of the model
      @param config {object}:
        init: function to call upon initialisation
    */
    createRestApi: function( model, config ) {
        var api = {};

        api.create = function( callback ) {
            $.ajax({
                url: '/api/' + model,
                type: 'PUT',
                success: function(response) {
                    callback(response);
                }
            });
        };

        api.save = function( id, data, callback ) {
            var url = ['/api', model, id].join('/');
            $.post(url, data, function(response){
                if( callback ) {
                    callback();
                }
            });
        };

        api.remove = function( id, callback ) {
            var url = ['/api', model, id].join('/');
            $.ajax({
                url: url,
                type: 'DELETE',
                success: function(response) {
                    if( callback ) {
                        callback();
                    }
                },
            });
        };
        api.init = config.init;

        api.init();

        return api;
    }, // createRestApi

}; // var core





$(document).ready( function() {

    var CardData = core.createRestApi('data', {
        init: function() {
            $('#add-data').click(function(){
                CardData.create(function(response) {
                    //$('#data-list').append(response);
                    //Card.init();
                });
            });
            core.createInputTimer({
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
    });



    var CardType = core.createRestApi('cardtype', {
        init: function() {
            $('#add-card-type').click(function(){
                $('#card-type-new-modal').modal('show');
                $('#new-card-type-name').focus();
            });
            core.createInputTimer({
                $elem: $('#new-card-type-name'),
                regex: /^[a-zA-Z\-]+$/,
                $errorElem: $('#new-cardtype-alert'),
                errorMessage: 'Name can only contain letters, and dashes',
                success: function( value ) {
                    $('button#card-type-new').attr('disabled', false);
                },
            });
            $('button#card-type-new').click(function(){
                $('#card-type-new-modal').modal('hide');
            });
            core.createInputTimer({
                $elem: $('.cardtype-name'),
                regex: /^[a-zA-Z\-]+$/,
                $errorElem: $('#cardtype-alert'),
                errorMessage: 'Name can only contain letters, and dashes',
                success: function( value ) {
                    var id = $('.cardtype-name').data('id');
                    CardType.save(id, {
                        name: value,
                    }, function() {
                        // empty
                    });
                },
            });
        },
    });

    var Field = {
        init: function() {
            $('.selectable-field').click(Field.click);

            $('#add-field').click(function(){
                Field.create();
            });
        },
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

                core.createInputTimer({
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
                core.createInputTimer({
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
                core.createInputTimer({
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
            $.post('/type/'+ cardType +'/new-card', {title: name}, function(response) {
                callback(response);
            });
        },
        open: function(id, callback) {
            $.get('/card/' + id, {}, function(response) {
                $('#card-edit-modal .modal-body').html(response);
                core.createInputTimer({
                    $elem: $('#card-name'),
                    regex: /^[a-zA-Z\- ]+$/,
                    $errorElem: $('#carddata-alert'),
                    errorMessage: 'Name can only contain letters, dashes, and spaces',
                });
                core.createInputTimer({
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
                data[$cardData[d].dataset.name] = $cardData[d].value;
            }
            var $cardFields = $('.card-field-value');
            var fields = {};
            for( var d=0; d<$cardFields.length; d++) {
                fields[$cardFields[d].dataset.name] = $cardFields[d].value;
            }

            Card.save(id, {
                title: name,
                count: count,
                data: data,
                fields: fields,
            }, function() {
                // update the row
                var $row = $('#card-'+id);
                $row.find('td.title').text(name);
                $row.find('td.count').text(count);
                // Set the data
                for( var name in data ) {
                    $row.find('td.data-'+name).text(data[name]);
                }
                // Set the fields
                for( var name in fields ) {
                    $row.find('td.field-'+name).text(fields[name]);
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
                Card.create( $name.data('cardtypeid'), $name.val(), function(row) {
                    $('.card-list tbody').append(row);
                    $('#card-new-modal').modal('hide');
                });
            });
            core.createInputTimer({
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


});






