

$(function() {
    var $categories = $('#category');
    var $cat_li = $('.cat-li');

    $cat_li.on('click', function (event) {
        $(this).find('ul').toggleClass('hidden');
    });


});