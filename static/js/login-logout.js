"use sctrict";


$.get('/loggedin', (res) => {

    if (res === true) {
        $('#login-button').click(function(){
            $('#login-out').attr('action', '/logout');
        });
    };
});

// function logInOut(evt) {
//     // if the button already says 'log-in':
//     if ($('#login-button').text()=== 'Log in') {
//         $('login-out').setAttribute("action", "/logout");
//         $('#login-button').html('Log out');
//         // change it to log-out

//     } else {
// ;       $('#login-button').html('Log in')
//         $('login-out').action('/login');}
//     // otherwise (if it says 'log-out') change it back to 'log-in'
// };

// // on the action of clicking the button, fun the logInOut function 
// $('#login-button').on('click', (logInOut));

// const navLogin = document.getElementById("login-button");
// const loginForm = document.getElementById("login-out");


// $.get('/loggedin', (res) => {

//     if (res === true) {
//         navLogin.innerHTML = "Log out";
//         loginForm.setAttribute("action", "/logout");
//     };
// });

// $('#login-button').on('click', (logInOut));


// $("#login-button").click(function(){
//     $("#login-out").att("action"),
// }) 

// $(document).ready(function(){
//     $('#login-trigger').click(function(){
//       $(this).next('#login-content').slideToggle();
//       $(this).toggleClass('active');

//       if ($(this).hasClass('active')) $(this).find('span').html('&#x25B2;')
//         else $(this).find('span').html('&#x25BC;')
//       })
//   });
