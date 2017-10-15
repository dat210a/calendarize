var modal = document.getElementById('myModal');

var login = document.getElementById('login_btn');
var signup = document.getElementById('signup_btn');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

signup.onclick = function(){
    modal.style.display = "flex"
    $('.collapsible').collapsible('open', 1);
}

login.onclick = function(){
    modal.style.display = "flex"
    $('.collapsible').collapsible('open', 0);
}