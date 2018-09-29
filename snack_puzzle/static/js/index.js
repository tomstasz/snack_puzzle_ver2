

$(function() {
    var $checkboxes = $('.form-check-input');
    var $ingredient_tabs = $('.ing-div');
    var $ingredients = [];
    var $check_btn = $('#check-btn');
    var $hide_btn = $('#hide-btn');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

    function remove_ingredient(array, ingredient) {
        var index = array.indexOf(ingredient);
        if(index === -1)
            return;

        array.splice(index, 1);
        remove_ingredient(array, ingredient)
    }

    $check_btn.on('click', function (event) {
        $checkboxes.prop('checked', false);
        $ingredients = [];
        console.log($ingredients);
    });

    $hide_btn.on('click', function (event) {
        $ingredient_tabs.removeClass('colapse show').addClass('collapse')
    });

    $checkboxes.each(function(index, element) {
        $(element).on('change', function(event) {
            if($(element).prop('checked')) {
                $ingredients.push($(element).data('name'));
                console.log($ingredients);
            } else if($(element).prop('checked', false)) {
                remove_ingredient($ingredients, $(element).data('name'));

                console.log($ingredients);
            }
            $.ajax({
                    url: 'http://127.0.0.1:8000',
                    method:'POST',
                    data: {sent_ingredients: $ingredients, csrfmiddlewaretoken: csrftoken}
                }).done(function (data) {
                    console.log(' success ingredients sent');
                    console.log(data);
                    console.log(JSON.parse(data))
                }).fail(function () {
                    console.log('failure ingredients sent')
                });

        })

    })




});