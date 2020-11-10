'use strict';

// This is from assessment 5 but could be used similarily. 

// jQuery.ajax({
//     url: 'https://pokeapi.co/api/v2/berry/',
//     type: 'GET',
//     dataType: 'json',
//     success: function(data){
        
//         // console.log(data); // for testing
//         let nameArray = data.results
//         //console.log(nameArray)

//         // looping through each item of the array and
//         // getting the first value (the name)
//         for (let name of nameArray) {
//             let berry = name.name
//             // console.log(name.name); // for testing
//             $('#berries').append(berry + ", ");
            
//             };

//         }
    
// });

// function limitChecks() {
//     $('.checkbox').click(function(evt) {
//         if ($('.checkbox:checked').length >= 3) {
//             $(".checkbox").not(":checked").attr("disabled",true);
//         }
//         else 
//             $(".checkbox").not(":checked").removeAttr('disabled');
//         });
// }
// function limitChecks() {
//     $('input[type=checkbox]').on('change', function(evt) {
//         if ($('input[type=checkbox]:checked').length > 3) {
//             $(this).prop('checked', false);
//             alert("Only 3 selections allowed.");
//         }
//     });
// }

// $('#topic-select').on('check', limitChecks)


// var checks = "park_search.html".querySelectorAll(".topic-check");
// var max = 3;
// for (var i = 0; i < checks.length; i++)
//     checks[i].onclick = selectiveCheck;

// function selectiveCheck (event) {
//     var checkedChecks = "park_search.html".querySelectorAll(".check:checked");
//     if (checkedChecks.length >= max + 1)
//         return false;
// }