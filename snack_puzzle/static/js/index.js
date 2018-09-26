

$(function() {
    var $checkboxes = $('.form-check-input');
    var $ingredients = [];

    function remove_ingredient(array, ingredient) {
        var index = array.indexOf(ingredient);
        if(index === -1)
            return;

        array.splice(index, 1);
        remove_ingredient(array, ingredient)
    }

    $checkboxes.each(function(index, element) {
        $(element).on('change', function(event) {
            if($(element).prop('checked')) {
                $ingredients.push($(element).data('name'));
                console.log($ingredients);
            } else if($(element).prop('checked', false)) {
                remove_ingredient($ingredients, $(element).data('name'));

                console.log($ingredients);
            }

        })

    })




});