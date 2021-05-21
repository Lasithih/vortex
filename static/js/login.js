function login() {
    var email = $("#login-username").val();
    if(email === '' || email === null) {
        alert("Please enter your username");
        return;
    }

    var password = $("#login-password").val();
    if(password === '' || password === null) {
        alert("Please enter your password");
        return;
    }

    var next = new URL(window.location.href).searchParams.get("next");
    var nextParam = '/';
    if(next !== null && typeof next !== 'undefined'){
        nextParam = next
    }


    $.ajax({
        url: "/api/v1/auth/login", //the page containing php script
        type: "POST", //request type,
        dataType: 'json',
        data: { username: email, password: password },
        success: function(result) {
            if(result.success) {
                window.location.href = nextParam;
                
            } else {
                alert("Username or password is incorrect");
            }
        },
        error(e) {
            console.log(e.responseText);
        }
    });
}