function gotoQuestion( question_id )
    {
    
    fetch("/questions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question_id: question_id })
    });
    alert( "Question Selected, click to continue!" );
    window.location = "/qna";
    }

