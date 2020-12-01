"use strict";


// function toggleExpand() {
//     var expanded = true;
//     $('img').each(function() {
//         if (!$(this).hasClass('expanded')) {
//             expanded = false;
//             return false;
//         }
//     });
//     $('a[href$=".png"], a[href$=".jpg"], a[href$=".gif"], a[href$=".bmp"]').children('img').each(function() {
//         if (expanded)
//             $(this).removeClass('expanded');
//         else
//             $(this).addClass('expanded');
//     });
// }

// $(function() {
//     $('.pop').on('click', function() {
//         $('.imagepreview').attr('src', $(this).find('img').attr('src'));
//         $('#imagemodal').modal('toggle');   
//     });		
// });

// $(".pop").on("click", function(e) {
//     // e.preventDefault() this is stopping the redirect to the image its self
//     e.preventDefault();
//     // #the-modal is the img tag that I use as the modal.
//     $('#imagemodal').modal('toggle');
// });

// $(".pop").on("click", function(e) {
//     // e.preventDefault() this is stopping the redirect to the image its self
//     e.preventDefault();
//     // #the-modal is the img tag that I use as the modal.
//     $('.imagepreview').attr('src', $(this).find('img').attr('src'));
//     $('#imagemodal').modal('toggle');
// });

// $(".pop").on("click", function(e) {
//     e.preventDefault();
//     $('.imagepreview').attr('src', $(this).find('img').attr('src'));
//     $('#imagemodal').modal('toggle');
//     $('#imagemodal').modal('show');
//     $('#imagemodal').modal({
//     keyboard: false
//     });

// });

// Get the modal
// var modal = document.getElementById("myModal");

// // Get the image and insert it inside the modal - use its "alt" text as a caption
// var img = document.getElementById("myImg");
// var modalImg = document.getElementById("img01");

// img.onclick = function(){
//     modal.style.display = "block";
//     modalImg.src = this.src;
// }

// // Get the <span> element that closes the modal
// var span = document.getElementsByClassName("close")[0];

// // When the user clicks on <span> (x), close the modal
// span.onclick = function() {
//     modal.style.display = "none";
// }