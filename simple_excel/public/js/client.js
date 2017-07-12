function SimpleExcelXBlock(runtime, xblockElement) {
    debugger;
    function handleSubmissionResult(results) {
	console.log('handleSubmissionResult INVOKED');
    	$(xblockElement).find('div[name=attempt-number]').text(results['attempt_number']);
    	$(xblockElement).find('div[name=problem-progress]').text(results['point_string']);
    	$(xblockElement).find('input[name=submit-button]').val("Submit")
    	if (results['submit_disabled'] == 'disabled') {
    		$(xblockElement).find('input[name=submit-button]').attr('disabled','disabled');
    	}
    	else
    	{
    		$(xblockElement).find('input[name=submit-button]').removeAttr('disabled'); 
    	}
    }
    /*
    var student_submit = function(data) {
        var handlerUrl = runtime.handlerUrl(xblockElement, 'student_submit');
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
    //$(element).find('.submission').bind( 'click', function(e){
    //	var student_answer ={ 'student_answer' :  $(element).find('.user_input_text').val() };
    //      student_submit(student_answer);
    //});
    */
    (xblockElement).find('input[name=submit-button]').bind('click', function() {
  		// accumulate student's answer for submission
  		
    	var data = {
      		'student_answer' :  $(xblockElement).find('.user_input_text').val()
    	};
    	
    	
    	/*console.log('student_answer: ' + data['student_answer']);
    	console.log('saved_question_template: ' + data['saved_question_template']);
    	console.log('serialized_variables: ' + data['saved_variables']);
    	console.log('serialized_generated_variables: ' + data['saved_generated_variables']);
    	console.log('saved_generated_question: ' + data['saved_generated_question']);
    	console.log('saved_answer_template: ' + data['saved_answer_template']);
    	console.log('saved_url_image: ' + data['saved_url_image']);*/
    	console.log('student_answer: ' + data["student_answer"]);
    	
        $(xblockElement).find('input[name=submit-button]').attr('disabled','disabled'); 
        $(xblockElement).find('input[name=submit-button]').val("Submitting...")
    	var handlerUrl = runtime.handlerUrl(xblockElement, 'student_submit');
    	$.post(handlerUrl, JSON.stringify(data)).success(handleSubmissionResult);
  	
    });



}
