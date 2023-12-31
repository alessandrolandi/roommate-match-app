$("form[name=register-form").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/register",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/register/survey";
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=survey-form").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/register/survey",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/home/";
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

$("form[name=login-form").submit(function(e) {
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "/",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp){
            window.location.href = "/home/";
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });

    e.preventDefault();
});

