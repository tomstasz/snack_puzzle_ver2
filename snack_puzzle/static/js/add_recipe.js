$(function() {
    var $button_recipe = $('#button_recipe');
    var $button_amount = $('#button_amount');
    var $form_amount = $("#form_amount");
    var $line = $('hr');

    $button_recipe.one('click', function(event) {
        event.preventDefault();
        $(this).attr('disabled', true);
        var $instruction = $('<h5>');
        $instruction.text("Pojedynczo dodawaj składniki do przepisu");
        $instruction.insertAfter($line);
        $form_amount.removeClass('hidden')
    })

});