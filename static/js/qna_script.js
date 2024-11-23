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

Sources: W3Schools, Decode.sh, Flask SocketIO Documentation
******************************************************************************/
/**************************************
Initialize a socket that will be used
to communciate with the game room
**************************************/
var socket = io( { closeOnBeforeunload: false } );

socket.on( "TEST MULTIPLAYER", () => { alert( "You are bad at programming lol" ) } );

/**************************************
Create a callback on the runButton on
the QNA page
**************************************/
document.getElementById('runButton').addEventListener( 'click', () => 
    {
    /**************************************
    Get the code that was in the text area
  * *************************************/
    const code = document.getElementById('code').value;
    
    var submit = { code: code };

    if( sessionStorage.getItem( "room_id" ) != null )
        {
        submit[ "room_id" ] = sessionStorage.getItem( "room_id" );
        }

    socket.emit( 'CODE SUBMIT', submit, (response) => { console.log(response);  socket.close(); location.reload() } );
    } );

/**************************************
Create a callback for when the language
is selected on the language selector
**************************************/
function lang_vals_on_click( lang_str )
    {
    const lang_button = document.getElementById( 'lang-button' );
    lang_button.textContent = lang_str;
    lang_button.innerText = lang_str;

    socket.emit( 'LANGUAGE SWITCH', { lang: lang_str }, (response) => { console.log(response);  socket.close(); location.reload() } );
    }

/**************************************
Textareas have this funny case where
the default value can't be changed once
it is set. Everytime the page is loaded
make sure to update the text area with
the correct value
**************************************/
window.onload = () => {
    document.getElementById('code').value = document.getElementById('code').defaultValue;
    if( sessionStorage.getItem( "room_id" ) != null )
        {
        socket.emit( 'HIDDEN JOIN ROOM', { room_id: sessionStorage.getItem( "room_id" ) }, ( response ) => { console.log( response ) } );
        }
}

document.getElementById('code').addEventListener("keydown", (e) => {
    if (e.key == "Tab") {
      e.preventDefault();
      const textArea = e.currentTarget;
      textArea.setRangeText(
        "\t",
        textArea.selectionStart,
        textArea.selectionEnd,
        "end"
      );
    }
  });
