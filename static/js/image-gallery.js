
// $('img').on('click', function(e) {
//     $('#imgViewer').html('').append( $(e.currentTarget).clone().removeClass('img-responsive').removeClass('img-thumbnail') )
//     $('#viewImg').modal('show')
// })

// $(document).ready(function () {
//     $('#image').on('click', function () {
//         (this).width($(this).width() * 2);
//     });
// })


// const displayedImage = document.querySelector('.displayed-img');
// const thumbBar = document.querySelector('.thumb-bar');

// const btn = document.querySelector('button');
// const overlay = document.querySelector('.overlay');

// /* Looping through images */
// let images = document.getElementById("gallery-view").value;


// for(let i=0;i<5;i++) {
//     const newImage = document.createElement('img');
//     newImage.setAttribute('src', images[i].image_url);
//     thumbBar.appendChild(newImage);
//     newImage.onclick=function(e){
//     displayedImage.src=e.target.src;
//     }
// }

//     /* Wiring up the Darken/Lighten button */
// btn.onclick=function(){
//     if (btn.classList.contains('dark')) {
//         btn.classList.add('light');
//         btn.textContent = 'Lighten';
//         overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
//         btn.classList.remove('dark');
//     } else {
//         btn.classList.add('dark');
//         btn.textContent = 'Darken';
//         overlay.style.backgroundColor = 'rgba(0,0,0,0)';
//     }
// });
// $(document).ready(function() {
//     var imageLinks = $('a[href$=".png"], a[href$=".jpg"], a[href$=".gif"], a[href$=".bmp"]');
//     if (imageLinks.children('img').length) {
//         imageLinks.children('img').each(function() {
//             var currentTitle = $(this).attr('title');
//             $(this).attr('title', currentTitle + ' (click to enlarge image)');
//         });
//         imageLinks.click(function(e) {
//             e.preventDefault();
//             $(this).children('img').toggleClass('expanded');
//         });
//     }
// });

function toggleExpand() {
    var expanded = true;
    $('img').each(function() {
        if (!$(this).hasClass('expanded')) {
            expanded = false;
            return false;
        }
    });
    $('a[href$=".png"], a[href$=".jpg"], a[href$=".gif"], a[href$=".bmp"]').children('img').each(function() {
        if (expanded)
            $(this).removeClass('expanded');
        else
            $(this).addClass('expanded');
    });
}