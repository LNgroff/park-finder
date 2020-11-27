'use strict';

// Looping through images:

// MDB Lightbox Init
$(function () {
    $("#mdb-lightbox-ui").load("mdb-addons/mdb-lightbox-ui.html");
    });



// $('input[type=checkbox]:checked').map(function(_, el) {
//     return $(el).val();
// }).get();

// $(document).ready(function () {

//     let choices = [];

//     $("input").click(function() {
//     if ($(this).is(':checked')) {
//         var checked = ($(this).val());
//         choices.push(checked);
//     } else {
//         choices.splice($.inArray(checked, choices),1);
//     }
//     });

//     $('#submit').on('click', function () {
//         alert(choices);
//         const chosen = jSON.stringify(choices)
//         return chosen
//     });

// });

// document.querySelector('form').addEventListener('submit', (evt) => {
//     evt.preventDefault();

//     let choices = [];

//     $("input").click(function() {
//     if ($(this).is(':checked')) {
//         var checked = ($(this).val());
//         choices.push(checked);
//     } else {
//         choices.splice($.inArray(checked, choices),1);
//     }
//     });

//     $('#submit').on('click', function () {
//         console.log(choices);
//     });

// });

// $('#{{ topic }}'}).click(function(){
//     let arr = $('topicCheckbox:checked').map(function(){
//         return this.value;
//     }).get();
// }); 


// $(document).ready(function() {
//     $(".btn_click").click(function(){
//         let chosenTopics = new Array();
//         $("input[name='topic']:checked").each(function() {
//             chosenTopics.push($(this).val());
//         });

//         alert("My favourite programming languages are: " + chosenTopics);
//     });
// });