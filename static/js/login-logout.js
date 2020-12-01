"use sctrict";



$(document).ready(function() {

    $('#login').hide();

    $('#show-login').on({
        click: function(){
            $('#login').toggle();

        }
    });

});

// $(document).ready(function() {

//     $('#attempt').on('click'){
//         alert("it worked!");
//     };
// });

// $( "#foo" ).on( "click", function() {
//     alert( $( this ).text() );});

// $( "#foo" ).trigger( "click" );