$(document).ready(function(){

    var check_task = function(check_url){
    /**
    Checks status of the task and redirects to results when it's done
    **/
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

    var submit_form = function(e){
    /**
        Submits form and runs task checking function
    **/
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

    };

    $('#query_form').submit(submit_form);
});
