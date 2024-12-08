/******************************************************************************
Module: pvp_script.js
Creation Date: November 21th, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga, Clare Channel

Description:
    This module is responsible for sending and handling callbacks when interacting
    with elements on the pvp page

Inputs:
    User Input

Outputs:
    None

Preconditions:
    The user is able to join a room

Postconditions:
    If a room is started, then they are playing the question within the context of a
    room

Error Conditions:
    None

Side Effects:
    None

Invariants:
    None
    
Known Faults:
    There have been issues with the autofill prevent the user from entering the
    code and joining the room

Sources: W3Schools, Decode.sh, Flask SocketIO Documentation
******************************************************************************/

/******************************************************************************
Variables
******************************************************************************/
/**************************************
Initialize a socket that will be used
to communciate with the game room
**************************************/
var socket = io( { closeOnBeforeunload: false } );

/******************************************************************************
SocketIO On Callback
******************************************************************************/
/* This callback is what the client should after joining a room
    which basically just gets all the people that are in the room
    and shows a list of socket ids. */
socket.on( 'JOIN ROOM POST', ( response ) => { 
    const waitingRoomList = document.getElementById('waiting-room-list');
    waitingRoomList.innerHTML = '';
    response["sids"].forEach(player => {
    waitingRoomList.innerHTML += player + "<br>";
} 
)});

/* The following call back is what the client should do after
    the host starts the party, which is load the questions page */
socket.on( 'START PARTY POST', ( response ) => { 
    socket.emit( 'START PARTY', { question_id: response[ "question_id" ], room_id: response[ "room_id" ], should_propagate: false }, ( response ) => { 
        console.log( response ); window.location="/qna" } )
});

/******************************************************************************
Procedures
******************************************************************************/
/* Get a list of all the anchor links on the page and an
   array that will store these links */
const aElements = document.querySelectorAll('a');
const links = [];

/* For each element in the page, remove the link and add it
   as a JS goto. On top of that, add an onclick that will
   basically indicate that a page was click and return the
   link that it should go to */
aElements.forEach( ( element, index ) => {
    var link = element.getAttribute( "href" );
    links.push( link );
    element.setAttribute( "href", "javascript:void(0)" );

    element.addEventListener('click', () => {            
        sessionStorage.setItem('linkClicked', true);
        sessionStorage.setItem( "link", links[ index ] );
        var id = sessionStorage.getItem( "room_id" );
        
        /* If a person was in a room and they click a link,
           remove the person from the room */
        if( id != null )
            {
            const waitingRoomList = document.getElementById('waiting-room-list');
            sessionStorage.removeItem( "room_id" );
            waitingRoomList.innerHTML = '';
            document.getElementById('room-code').value = '';
            
            /* Tell the server to leave the room */
            socket.emit( 'LEAVE ROOM', { room_id: id }, ( response ) => { 
                console.log( response );
                window.onbeforeunload();
                } );
            }
        else
            {
            /* Otherwise, just trigger a page unload */
            window.onbeforeunload();
            }

        
        });
});

/* When the question vals button is clicked, replace the
   the text of the button with the selected selection */
function question_vals_on_click( question, value )
    {
    const active = document.getElementById( 'active-question' );
    active.innerHTML = question;
    active.innerText = question;
    active.setAttribute( "value", value )
    }


document.getElementById('room-code').addEventListener("keydown", (e) => {
    if (e.key == "Enter") {
        e.preventDefault();
        var code = document.getElementById('room-code').value;
        if( sessionStorage.getItem( "room_id" ) == code )
            {
            return;
            }

        /* Tell the server to join the room*/
        socket.emit( 'JOIN ROOM', { room_id: code }, ( response ) => { console.log( response ) } );
        sessionStorage.setItem( "room_id", code );
    }
    });

// Handle Start Party
document.getElementById('start-button').addEventListener('click', () => {
    const question = document.getElementById( 'active-question' ).getAttribute( 'value' );
    const room_id = sessionStorage.getItem( "room_id" );
    if( room_id != null )
        {
            socket.emit( 'START PARTY', { question_id: question, room_id: room_id, should_propagate: true }, ( response ) => { console.log( response ); window.location="/qna" } )
        }
});

/**************************************
Set a callback for whenthe window loads
**************************************/
window.onload = () => {
    if( sessionStorage.getItem( "room_id" ) != null )
        {
        /* Basically, if a room already exists for this user, force them
           into the room and hide all the room configuration buttons */
        socket.emit( 'JOIN ROOM', { room_id: sessionStorage.getItem( "room_id" ) }, ( response ) => { console.log( response ) } );
        document.getElementById('room-code').value = sessionStorage.getItem( "room_id" );
        }
};

/* This is the callback for when the page is reloaded or
   exited */
window.onbeforeunload = () => {
    var cond1 = window.performance.getEntriesByType( 'navigation' )[0].type == 'reload';
    var cond2 = Boolean( sessionStorage.getItem( "linkClicked" ) == "true" );
    if( cond2 )
        {
        /* If a link was clicked, remove the player from the room */
        const waitingRoomList = document.getElementById('waiting-room-list');
        sessionStorage.removeItem( "room_id" );
        waitingRoomList.innerHTML = '';
        document.getElementById('room-code').value = '';
        }
    sessionStorage.setItem( "linkClicked", false );

    /* Only trigger a page link transition if there is a link that exists */
    var link = sessionStorage.getItem( "link" );
    if( link != null )
        {
        sessionStorage.removeItem( "link" );
        window.location = link;
        }
};

window.pagehide = () =>
    {
    socket.close();
    }

    