var modal = document.getElementById('myModal');

var login = document.getElementById('login_btn');
var signup = document.getElementById('signup_btn');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        signup.style.display = "block";
        login.style.display = "block";
        $('.collapsible').collapsible('close', 0);
        $('.collapsible').collapsible('close', 1);
    }
}

signup.onclick = function(){
    signup.style.display = "none";
    login.style.display = "none";
    modal.style.display = "flex";
    $('.collapsible').collapsible('open', 1);
}

login.onclick = function(){
    signup.style.display = "none";
    login.style.display = "none";
    modal.style.display = "flex";
    $('.collapsible').collapsible('open', 0);
}

$('#btnLogin').click(function(e){
    $.ajax({
        url: '/login',
        data: $('#formLogin').serialize(),
        type: 'POST',
        success: function(response) {
            if (response == "false"){
                $('#loginEmail').addClass("validate invalid")
                            .keyup(function(){
                                $(this).removeClass('validate invalid');
                                $('#loginPassword').removeClass('validate invalid');
                            });
                $('#loginPassword').addClass("validate invalid")
                            .keyup(function(){
                                $(this).removeClass('validate invalid');
                                $('#loginEmail').removeClass('validate invalid');
                            });
            }
            else
                window.location = response;

        },
        error: function(error) {
            console.log(error);
        }
    });
    return false;
});

$('#registerEmail').bind('blur keyup', function(e){
    if (e.type == 'blur' || e.keyCode == '13'){
        $.ajax({
            url: '/user_availability',
            data: {'inputEmail': $('#registerEmail')[0].value},
            type: 'POST',
            success: function(response) {
                if (response == 'false'){
                    $('#regEmailLabel').attr('data-error', 'User already exists, try logging in.');
                    $('#registerEmail')
                        .addClass('invalid')
                        .keyup(function(){
                            $(this).removeClass('invalid');
                            $('#regEmailLabel').attr('data-error', 'Not a valid email address.');
                        });
                };
            },  
            error: function(error) {
            }
        });
    };
});

