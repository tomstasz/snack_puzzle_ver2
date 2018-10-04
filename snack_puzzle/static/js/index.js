

$(function() {
    var $checkboxes = $('.form-check-input');
    var $ingredient_tabs = $('.ing-div');
    var $ingredients = [];
    var $check_btn = $('#check-btn');
    var $hide_btn = $('#hide-btn');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var $recipe_nav = $('#recipe_nav');
    var $scroll_area = $('#scroll_area');


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
        $recipe_nav.empty();
        $scroll_area.empty();
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
                $recipe_nav.empty();
                $scroll_area.empty();
            } else if($(element).prop('checked', false)) {
                remove_ingredient($ingredients, $(element).data('name'));
                $recipe_nav.empty();
                $scroll_area.empty();

                console.log($ingredients);
            }
            $.ajax({
                    url: 'http://127.0.0.1:8000',
                    method:'POST',
                    data: {sent_ingredients: $ingredients, csrfmiddlewaretoken: csrftoken}
                }).done(function (data) {
                    console.log('success ingredients sent');
                    console.log(data);
                    console.log(JSON.parse(data));
                    data = JSON.parse(data);

                    for(var i = 0; i < data.length; i++) {

                        if (data[i].length === 0) {
                            console.log("Nie ma takiego przepisu");

                        } else {
                            console.log(data[i]);
                            var $new_card_container = $("<div id='recipe_" + data[i].id +
                                "' class='card container-fluid mb-4' style='width: 25rem'>");
                            var $new_card_body = $("<div class='card-body'>");
                            var $new_card_title = $("<h3 class='card-title'>" + data[i].name + "</h3>");
                            var $new_card_subtitle = $("<h5 class='card-subtitle text-muted pb-3'>" + data[i].time
                                + " min.</h5>");
                            var $new_card_text = $("<p class='card-text'>" + data[i].description + "</p>");
                            var $new_ingredient_list = $("<ul class='list-group list-group-flush'>");

                            $recipe_nav.append($("<li><a href='#recipe_"+ data[i].id +"'>" + data[i].name + "</a></li>"));
                            $scroll_area.append($new_card_container);
                            $new_card_container.append($new_card_body);
                            $new_card_body.append($new_card_title).
                            append($new_card_subtitle).
                            append($new_card_text).
                            append($new_ingredient_list);
                            console.log(data[i].ingredient_recipe);
                            var $ing_in_recipe = data[i].ingredient_recipe;
                            for(var j= 0; j < $ing_in_recipe.length; j++) {
                                var $new_li = $("<li class='list-group-item'>");
                                var $new_span = $("<span class='float-right'>");
                                $new_span.text($ing_in_recipe[j].amount + ' ' + $ing_in_recipe[j].measure);
                                $new_li.text($ing_in_recipe[j].ingredient.name);
                                $new_li.append($new_span);
                                $new_ingredient_list.append($new_li);

                            }
                            var $new_card_body_link = $("<div class='card-body'>");
                            var $new_link = $("<a href='" + data[i].url + "' class='card-link'>Zobacz przepis</a>");
                            $new_card_container.append($new_card_body_link);
                            $new_card_body_link.append($new_link);
                        }
                    }

                }).fail(function () {
                    console.log('failure ingredients sent')
                });

        })

    })




});