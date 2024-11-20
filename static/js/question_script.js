/******************************************************************************
Module: question_script.js
Creation Date: November 9th, 2024
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
    The user selects a question

Postconditions:
    The page shifts to another page to answer question

Error Conditions:
    None

Side Effects:

Invariants:

Known Faults:
    None

Sources: W3Schools
******************************************************************************/

/**************************************
Create a callback for every element in
the questions list
**************************************/
function gotoQuestion( question_id )
    {
    /**************************************
    Send the selected question back to the
    server
    **************************************/
    var socket = io();
    socket.emit( 'QUESTION SELECTION', { question_id: question_id }, (response) => { console.log(response);  socket.close(); window.location = "/qna"; } );
    }

