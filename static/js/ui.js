/*
 * The GUI functionality to use the REST API
 */

// Create the namespace instance
let ns = {};
let api_path = "api/v1/"

// Create the model instance
ns.model = (function() {
    'use strict';

    let $event_pump = $('body');

    // Return the API
    return {
        'read': function() {
            let ajax_options = {
                type: 'GET',
                url: api_path+'labTests',
                accepts: 'application/json',
                dataType: 'json'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_read_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        create: function(labTest) {
            let ajax_options = {
                type: 'POST',
                url: api_path+'labTests',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(labTest)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_create_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        update: function(labTest, test_id) {

            let ajax_options = {
                type: 'PUT',
                url: api_path+`labTests/${test_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(labTest)
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_update_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        },
        'delete': function(test_id) {
            let ajax_options = {
                type: 'DELETE',
                url: api_path+`labTests/${test_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            $.ajax(ajax_options)
            .done(function(data) {
                $event_pump.trigger('model_delete_success', [data]);
            })
            .fail(function(xhr, textStatus, errorThrown) {
                $event_pump.trigger('model_error', [xhr, textStatus, errorThrown]);
            })
        }
    };
}());

// Create the view instance
ns.view = (function() {
    'use strict';

    let $test_id = $('#test_id'),
        $name = $('#name'),
        $unit = $('#unit'),
        $value_min = $('#value_min'),
        $value_max = $('#value_max');

    // return the API
    return {
        reset: function() {
            $test_id.val('');
            $name.val('');
            $unit.val('');
            $value_min.val('');
            $value_max.val('').focus();

        },
        update_editor: function(labTest) {
            $test_id.val(labTest.test_id);
            $name.val(labTest.name);
            $unit.val(labTest.unit);
            $value_min.val(labTest.value_min);
            $value_max.val(labTest.value_max).focus();
        },
        build_table: function(labTest) {
            let rows = ''

            // Check if the table was retrieved
            if (labTest) {
                // clear the table
                $('#labTest_table table > tbody').empty();

                for (let i=0, l=labTest.length; i < l; i++) {
                    rows += `<tr test_id="${labTest[i].test_id}">
                        <td class="name">${labTest[i].name}</td>
                        <td class="unit">${labTest[i].unit}</td>
                        <td class="value_min">${labTest[i].value_min}</td>
                        <td class="value_max">${labTest[i].value_max}</td>
                    </tr>`;
                }
                $('table > tbody').append(rows);
            }
        },
        error: function(error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function() {
                $('.error').css('visibility', 'hidden');
            }, 3000)
        }
    };
}());

// Create the controller
ns.controller = (function(m, v) {
    'use strict';

    let model = m,
        view = v,
        $event_pump = $('body'),
        $test_id = $('#test_id'),
        $name = $('#name'),
        $unit = $('#unit'),
        $value_min = $('#value_min'),
        $value_max = $('#value_max');

    // Get the data from the model after the controller is done initializing
    setTimeout(function() {
        model.read();
    }, 100)

    // Validate input
    function validate(name, unit) {
        return name !== "" && unit !== "";
    }

    // Create our event handlers
    $('#create').click(function(e) {
        let name = $name.val(),
            unit = $unit.val(),
            value_min = $value_min.val(),
            value_max = $value_max.val();

        e.preventDefault();

        if (validate(name, unit)) {
            model.create({
                'name': name,
                'unit': unit,
                'value_min': value_min,
                'value_max': value_max
            })
        } else {
            alert('Name or unit cannot be empty');
        }
    });

    $('#update').click(function(e) {
        let test_id = $test_id.val(),
            name = $name.val(),
            unit = $unit.val(),
            value_min = $value_min.val(),
            value_max = $value_max.val();

        e.preventDefault();

        if (validate(name, unit)) {
            model.update({
                name: name,
                unit: unit,
                value_min: value_min,
                value_max: value_max
            }, test_id)
        } else {
            alert('Name or unit cannot be empty');
        }
        e.preventDefault();
    });

    $('#delete').click(function(e) {
        let test_id = $test_id.val();

        e.preventDefault();
        model.delete(test_id)

        e.preventDefault();
    });

    $('#reset').click(function() {
        view.reset();
    })

    $('table > tbody').on('dblclick', 'tr', function(e) {
        let $target = $(e.target).parent();
        $("tr").removeClass("table-primary");
        $(e.target).parent().addClass("table-primary")
        view.update_editor({
            test_id: $target.attr('test_id'),
            name: $target.find('td.name').text(),
            unit: $target.find('td.unit').text(),
            value_min: $target.find('td.value_min').text(),
            value_max: $target.find('td.value_max').text(),
        });
    });

    // Handle the model events
    $event_pump.on('model_read_success', function(e, data) {
        view.build_table(data);
        view.reset();
    });

    $event_pump.on('model_create_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_update_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_delete_success', function(e, data) {
        model.read();
    });

    $event_pump.on('model_error', function(e, xhr, textStatus, errorThrown) {
        let error_msg = textStatus + ': ' + errorThrown + ' - ' + xhr.responseJSON.detail;
        view.error(error_msg);
        console.log(error_msg);
    })
}(ns.model, ns.view));