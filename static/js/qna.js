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

socket.on( "TEST MULTIPLAYER", ( response ) => { alert( "You got #" + response[ "position" ] + "!" ); window.location="/home" } );

/**************************************
Create a callback on the runButton on
the QNA page
**************************************/
document.getElementById("run-code").addEventListener( 'click', () => 
    {
    /**************************************
    Get the code that was in the text area
    *************************************/
    const code = document.getElementById('code-box').innerText;
    
    var submit = { code: code };

    if( sessionStorage.getItem( "room_id" ) != null )
        {
        submit[ "room_id" ] = sessionStorage.getItem( "room_id" );
        }
    document.getElementById('popup').style.display = 'flex'
    socket.emit( 'CODE SUBMIT', submit, (response) => { console.log(response);  document.getElementById('popup').style.display = 'none'; socket.close(); location.reload() } );
    } );

/**************************************
Create a callback for when the language
is selected on the language selector
**************************************/
document.getElementById( "lang-button" ).addEventListener( 'change', () => {
    var element = document.getElementById( "lang-button" );
    socket.emit( 'LANGUAGE SWITCH', { lang: element.value }, (response) => { console.log(response);  socket.close(); location.reload() } );
} );

/**************************************
Textareas have this funny case where
the default value can't be changed once
it is set. Everytime the page is loaded
make sure to update the text area with
the correct value
**************************************/
window.onload = () => {
    if( sessionStorage.getItem( "room_id" ) != null )
        {
        socket.emit( 'HIDDEN JOIN ROOM', { room_id: sessionStorage.getItem( "room_id" ) }, ( response ) => { console.log( response ) } );
        }
}

/* https://www.eddymens.com/blog/how-to-allow-the-use-of-tabs-in-a-textarea
Basically this is logic to allows tabs to be inputted into a text area */
document.getElementById('code-box').addEventListener("keydown", (e) => {
    if (e.key == "Tab") {
        e.preventDefault();
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const tabNode = document.createTextNode('\t');
        range.insertNode(tabNode);
        range.setStartAfter(tabNode);
        range.setEndAfter(tabNode);
        selection.removeAllRanges();
        selection.addRange(range);
    }
    if (e.key == "Enter") {
        e.preventDefault();
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const tabNode = document.createTextNode('\n'); // 4 non-breaking spaces
        range.insertNode(tabNode);
        range.setStartAfter(tabNode);
        range.setEndAfter(tabNode);
        selection.removeAllRanges();
        selection.addRange(range);
    }
  });
