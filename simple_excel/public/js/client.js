function SimpleExcelXBlock(runtime, element) {
    debugger;
    var student_submit = function(data) {
        var handlerUrl = runtime.handlerUrl(element, 'student_submit');
        runtime.notify('submit', {state: 'start', message: gettext("Submitting")});
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            dataType: "json",
            success: function(response) { runtime.notify('submit', {state: 'end'}); }
        }).fail(function(jqXHR) {
            var message = gettext("This may be happening because of an error with our server or your internet connection. Try refreshing the page or making sure you are online.");
            if (jqXHR.responseText) { // Is there a more specific error message we can show?
                try {
                    message = JSON.parse(jqXHR.responseText).error;
                    if (typeof message === "object" && message.messages) {
                        // e.g. {"error": {"messages": [{"text": "Unknown user 'bob'!", "type": "error"}, ...]}} etc.
                        message = $.map(message.messages, function(msg) { return msg.text; }).join(", ");
                    }
                } catch (error) { message = jqXHR.responseText.substr(0, 300); }
            }
            runtime.notify('error', {title: gettext("Unable to update settings"), message: message});
        });
    };
    $(element).find('.submission').bind( 'click', function(e){
	var student_answer ={ 'student_answer' :  $(element).find('.user_input_text').val() };
        student_submit(student_answer);
    });
}
