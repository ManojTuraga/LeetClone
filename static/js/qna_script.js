/******************************************************************************
Module: qna_script.js
Creation Date: October 22th, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga

Description:
    This module will contain callbacks for elements that are on the qna page.
    The result of these callbacks being triggered is a modification on the 
    state of the page.

Inputs:
    User Input

Outputs:
    None

Preconditions:
    The user clicks the run button on the page

Postconditions:
    The code is submitted to the server for processing

Error Conditions:
    None

Side Effects:
    Will lead to a modification to show what test cases failed

Invariants:
    The 'runButton' element must exist on the page

Known Faults:
    None

Sources: W3Schools
******************************************************************************/

/**************************************
Create a callback on the runButton on
the QNA page
**************************************/
document.getElementById('runButton').addEventListener('click', () => {
  /**************************************
  Get the code that was in the text area
  **************************************/
  const code = document.getElementById('code').value;
  
  const lang_button = document.getElementById( 'lang-button' );
  const prompt = document.getElementById( 'promptBox' );
  const q_id = prompt.getAttribute( "value" );
  
  const lang = lang_button.textContent || lang_button.innerText;
  
  /**************************************
   Send the information to the server for
   processing
   **************************************/
  response = fetch("/qna", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ code: code, lang: lang, question_id: q_id, type: "code_submit" })
    });
    alert( "Code Submittied, Click to see results!" );
    location.reload();
});

function lang_vals_on_click( lang_str )
    {
        const lang_button = document.getElementById( 'lang-button' );
        lang_button.textContent = lang_str;
        lang_button.innerText = lang_str;

        
        const prompt = document.getElementById( 'promptBox' );
        const q_id = prompt.getAttribute( "value" );
        
        fetch("/qna", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ lang: lang_str, question_id: q_id, type: "lang_switch" })
        });
        
        alert( "Language Changed, Click to Update!" );
        location.reload();
    }

window.onload = () => {
    document.getElementById('code').value = document.getElementById('code').defaultValue;
}
