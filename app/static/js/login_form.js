// toggle login/registration screen
window.onclick = function(e){
    if (e.target == $('#login_form')[0]){
        toggle()
        $('.collapsible').collapsible('close', 0);
        $('.collapsible').collapsible('close', 1);
    }
 }

$('#signup_btn').click(function(){
    toggle()
    $('.collapsible').collapsible('open', 1);
})

$('#login_btn').click(function(){
    toggle()
    $('.collapsible').collapsible('open', 0);
})

function toggle(){
    $('#myModal, #login_btn, #signup_btn').toggle();
}

// check for credentials at login
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


// check for existing user based on email when registering
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

