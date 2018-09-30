

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
                    console.log(JSON.parse(data));
                    data = JSON.parse(data);
                    var $recipe_nav = $('#recipe_nav');
                    var $scroll_area = $('#scroll_area');
                    for(var i = 0; i < data.length; i++) {
                        if (data[i].length === 0) {
                            console.log("Nie ma takiego przepisu");
                        } else {
                            console.log(data[i]);
                            var $new_card_container = $("<div id='" + data[i].id + "' class='card container-fluid'>");
                            var $new_card_body = $("<div class=card-body>");
                            var $new_card_title = $("<h3 class='card-title'>" + data[i].name + "</h3>");
                            var $new_card_subtitle = $("<h5 class='card-subtitle text-muted'>" + data[i].time + "</h5>");
                            var $new_card_text = $("<p>" + data[i].description + "</p>");
                            var $new_ingredient_list = $("<ul class='list-group list-group-flush'>");

                            $recipe_nav.append($("<li><a href='#"+ data[i].id +"'>" + data[i].name + "</a></li>"));
                            $scroll_area.append($new_card_container).
                            append($new_card_body).
                            append($new_card_title).
                            append($new_card_subtitle).
                            append($new_card_text).append($new_ingredient_list);
                            for(var j= 0; j < data[i].ingredient_recipe.length; j++) {
                                $new_ingredient_list.append($("<li class='list-group-item'>" + data[i].ingredient_recipe[j].name + "</li>"))
                            }
                        }
                    }

                }).fail(function () {
                    console.log('failure ingredients sent')
                });

        })

    })




});