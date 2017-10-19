var modal = document.getElementById('myModal');

var login = document.getElementById('login_btn');
var signup = document.getElementById('signup_btn');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        signup.style.display = "block"
        login.style.display = "block"
        $('.collapsible').collapsible('close', 0);
        $('.collapsible').collapsible('close', 1);
    }
}

signup.onclick = function(){
    signup.style.display = "none"
    login.style.display = "none"
    modal.style.display = "flex"
    $('.collapsible').collapsible('open', 1);
}

login.onclick = function(){
    signup.style.display = "none"
    login.style.display = "none"
    modal.style.display = "flex"
    $('.collapsible').collapsible('open', 0);
}

// $('#formLogin').click(function(e){
//     e.preventDefault()
//     $.ajax({
//         url: '/login',
//         data: $(this).serialize(),
//         type: 'POST',
//         success: function(response) {
//             console.log(response, this)
//             r = JSON.parse(response)
//             if (r['success'] == true)
//                 $('#formLogin').submit()
//         },
//         error: function(error) {
//             console.log(error)
//         }
//     });
// })

// $('#formRegister').on('submit', function(e){
//     e.preventDefault()
//     $.ajax({
//         url: '/register',
//         data: $(this).serialize(),
//         type: 'POST',
//         success: function(response) {
//             document.write(response);
//         },
//         error: function(error) {
//             document.write(error);
//         }
//     });
// })

    //TESTS
    // var email = document.getElementById("inputEmail")
    // email.classList.remove("valid")
    // email.classList.add("invalid")

    // var email = document.getElementById("inputEmail"), 
    //     confirm_email = document.getElementById("confirm_email");
    // var password = document.getElementById("inputPassword"), 
    //     confirm_password = document.getElementById("confirm_password");

    // if (PasswordStrength(password.value)){
    //     console.log('match')
    // }
    // else{
    //     password.setCustomValidity("not strong");
    // }

    // confirm_email.setCustomValidity("");
    // confirm_password.setCustomValidity("");

    // if(email.value != confirm_email.value) {
    //     confirm_email.setCustomValidity("Emails Don't Match");
    //     console.log('email')
    //     return false
    // } else if (password.value != confirm_password.value){
    //     confirm_password.setCustomValidity("Passwords Don't Match");
    //     console.log('pass')
    //     return false
    // } else{
    //     console.log('send')
    //     return false;