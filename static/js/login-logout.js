"use sctrict";


$(document).ready(function() {

    $('#login').hide();

    $('#show-login').on({
        click: function(){
            $('#login').toggle();

        }
    });

});