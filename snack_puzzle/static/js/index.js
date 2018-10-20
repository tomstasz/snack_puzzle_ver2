

$(function() {
    var $checkboxes = $('.check');
    var $ingredient_tabs = $('.ing-div');
    var $ingredients = [];
    var $check_btn = $('#check-btn');
    var $hide_btn = $('#hide-btn');
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    var $recipe_nav = $('#recipe_nav');
    var $scroll_area = $('#scroll_area');
    var $num_fields = $('.num');
    var $select_fields = $('.select');


    event_handler($num_fields);
    event_handler($select_fields);


    function event_handler(element) {
        element.on('change', function(event) {
            $(this).siblings('.check').removeClass('hidden')

        });
    }

    function random_phrase() {
        var phrases = ["Marsz do sklepu!", "Przetrząśnij kuchnię!", "Czas na zakupy!", "Może sąsiad pożyczy?"];
        return phrases[Math.floor(Math.random() * phrases.length)];
    }

    function remove_ingredient(array, ingredient) {
        array.forEach(function(element, index) {
            if (element.name === ingredient) {
                array.splice(index, 1)
            }

        });
        var check = array.some(function(element) {
            return element.name === ingredient;
        });
        if (check ) {
            remove_ingredient(array, ingredient)
        }

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

    $recipe_nav.on('click', 'a', function (event) {
        $ingredient_tabs.removeClass('colapse show').addClass('collapse')
    });


    $checkboxes.each(function(index, element) {
        $(element).on('change', function(event) {
            if($(element).prop('checked')) {
                var $ing_obj = {};
                var $ing_name = $(element).data('name');
                var $ing_amount = $(element).prev().prev().val();
                var $ing_measure = $(element).prev().val();
                $ing_obj.name = $ing_name;
                $ing_obj.amount = $ing_amount;
                $ing_obj.measure = $ing_measure;
                console.log($ing_obj);
                $ingredients.push($ing_obj);
                console.log($ingredients);
                $recipe_nav.empty();
                $scroll_area.empty();
            } else if($(element).prop('checked', false)) {
                remove_ingredient($ingredients, $(element).data('name'));

                $recipe_nav.empty();
                $scroll_area.empty();

                console.log($ingredients);
            }
            var data = JSON.stringify({ingredients: $ingredients});
            $.ajax({
                    url: 'http://127.0.0.1:8000',
                    method:'POST',
                    data: {data: data, csrfmiddlewaretoken: csrftoken},
                }).done(function (data) {
                    console.log('success ingredients sent');
                    console.log(data);
                    console.log(JSON.parse(data));
                    data = JSON.parse(data);


                    for(var i = 0; i < data.serial.length; i++) {

                        if (data.serial[i].length === 0) {
                            console.log("Nie ma takiego przepisu");

                        } else if (data.measure.length > 0){
                            for(var k = 0; k < data.measure.length ; k++) {
                                swal({
                                      title: "Jesteś blisko przepisu na "
                                          + data.measure[k].recipe_name.toUpperCase()
                                          + "!",
                                      text: "Spróbuj innej miary dla składnika "
                                          + data.measure[k].ingredient_name.toUpperCase(),
                                      icon: "info"
                                    });

                            }

                        } else if (data.amount.length > 0){
                            for(var l = 0; l < data.amount.length ; l++) {
                                swal({
                                      title: "Masz trochę za mało składnika " +
                                          data.amount[l].ingredient_name.toUpperCase() +
                                          ", by zrobić " + data.amount[l].recipe_name.toUpperCase()
                                          + "!",
                                      text: random_phrase(),
                                      icon: "warning"
                                    });
                            }

                        } else {

                            var $new_card_container = $("<div id='recipe_" + data.serial[i].id +
                                "' class='card container-fluid mb-4' style='width: 25rem'>");
                            var $new_card_body = $("<div class='card-body'>");
                            var $new_card_title = $("<h3 class='card-title'>" + data.serial[i].name + "</h3>");
                            var $new_card_subtitle = $("<h5 class='card-subtitle text-muted pb-3'>" + data.serial[i].time
                                + " min.</h5>");
                            var $new_card_text = $("<p class='card-text'>" + data.serial[i].description + "</p>");
                            var $new_ingredient_list = $("<ul class='list-group list-group-flush'>");

                            $recipe_nav.append($("<li><a class='nav_a' href='#recipe_"+ data.serial[i].id +"'>" + data.serial[i].name + "</a></li>"));
                            $scroll_area.append($new_card_container);
                            $new_card_container.append($new_card_body);
                            $new_card_body.append($new_card_title).
                            append($new_card_subtitle).
                            append($new_card_text).
                            append($new_ingredient_list);
                            console.log(data.serial[i].ingredient_recipe);
                            var $ing_in_recipe = data.serial[i].ingredient_recipe;
                            for(var j= 0; j < $ing_in_recipe.length; j++) {
                                var $new_li = $("<li class='list-group-item'>");
                                var $new_span = $("<span class='float-right'>");
                                $new_span.text($ing_in_recipe[j].amount + ' ' + $ing_in_recipe[j].measure);
                                $new_li.text($ing_in_recipe[j].ingredient.name);
                                $new_li.append($new_span);
                                $new_ingredient_list.append($new_li);

                            }
                            var $new_card_body_link = $("<div class='card-body'>");
                            var $new_link = $("<a href='" + data.serial[i].url + "' class='card-link'>Zobacz przepis</a>");
                            $new_card_container.append($new_card_body_link);
                            $new_card_body_link.append($new_link);

                        }
                    }

                }).fail(function () {
                    console.log('failure ingredients sent')
                });

        })

    });





});