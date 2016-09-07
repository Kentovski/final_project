$(document).ready(function(){

    var check_task = function(check_url){
        $.ajax({
            type: "GET",
            url: check_url,
            success: function (data) {
                if(data.is_done === true){
                    window.location=data.results_url
                } else {
                   // 30 sec past (max loop)
                };
            },
            error: function(data) {
                console.log(data);
            },
            dataType: "json",
            timeout: 30000
        });
    };

    $('#query_form').submit(function(e) {

        $('#submit_button').prop('disabled', true);

        $.ajax({
               type: "POST",
               url: $('#query_form').attr('action'),
               data: $("#query_form").serialize(), // serializes the form's elements.
               success: function(data)
               {
                   if (data.status == "success"){
                        check_task(data.check_url);
                   } else {
                        alert('Failed to do the request');
                   };
               }
             });
        e.preventDefault();
    });
});
