/******************************************************************************
Module: qna_script.js
Creation Date: November 19th, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga, Clare Channel

Description:

Inputs:
    User Input

Outputs:
    None

Preconditions:

Postconditions:

Error Conditions:
    None

Side Effects:

Invariants:

Known Faults:
    None

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
socket.on( 'JOIN ROOM POST', ( response ) => { 
    const waitingRoomList = document.getElementById('waiting-room-list');
    waitingRoomList.innerHTML = '';
    response["sids"].forEach(player => {
    const listItem = document.createElement('li');
    listItem.style.color = "black";
    listItem.textContent = player;
    waitingRoomList.appendChild(listItem);
} 
)});

socket.on( 'START PARTY POST', ( response ) => { 
    socket.emit( 'START PARTY', { question_id: response[ "question_id" ], room_id: response[ "room_id" ], should_propagate: false }, ( response ) => { console.log( response ); window.location="/qna" } )
});

/******************************************************************************
Procedures
******************************************************************************/
const aElements = document.querySelectorAll('a');
const links = [];

aElements.forEach( ( element, index ) => {
    var link = element.getAttribute( "href" );
    links.push( link );
    element.removeAttribute( "href" );

    element.addEventListener('click', () => {
        if( element.id != "activepage" )
            {
            sessionStorage.setItem('linkClicked', true);
            sessionStorage.setItem( "link", links[ index ] );
            }
    
        var id = sessionStorage.getItem( "room_id" );

        if( id != null )
            {
            const waitingRoomList = document.getElementById('waiting-room-list');
            sessionStorage.removeItem( "room_id" );
            waitingRoomList.innerHTML = '';
            document.getElementById('join-code').value = '';
            
            socket.emit( 'LEAVE ROOM', { room_id: id }, ( response ) => { 
                console.log( response );
                window.onbeforeunload();
                } );
            }
        else
            {
            window.onbeforeunload();
            }

        
        });
});

function question_vals_on_click( question, value )
    {
    const quest_button = document.getElementById( 'question-button' );
    quest_button.textContent = question;
    quest_button.innerText = question;
    quest_button.value = value;
    }

function player_type_on_click( type )
    {
    const type_button = document.getElementById( 'player-type' );
    const quest_button = document.getElementById( 'question-button' );
    const start_button = document.getElementById( 'start-button' );
    type_button.textContent = type;
    type_button.innerText = type;

    if( type == "Join" )
        {
        quest_button.style.display = "none";
        start_button.style.display = "none";
        }
    else
        {
        quest_button.style.display = "block";
        start_button.style.display = "block";
        }

    }

document.getElementById('join-button').addEventListener('click', () => {
    const code = document.getElementById('join-code').value;
    if( sessionStorage.getItem( "room_id" ) == code )
        {
        return;
        }
    const type_button = document.getElementById( 'player-type' );
    const quest_button = document.getElementById( 'question-button' );
    type_button.style.display = "none";
    quest_button.style.display = "none";
    socket.emit( 'JOIN ROOM', { room_id: code }, ( response ) => { console.log( response ) } );
    sessionStorage.setItem( "room_id", code );
} );

// Handle Start Party
document.getElementById('start-button').addEventListener('click', () => {
    const question = document.getElementById( 'question-button' ).getAttribute( 'value' );
    const room_id = sessionStorage.getItem( "room_id" );
    socket.emit( 'START PARTY', { question_id: question, room_id: room_id, should_propagate: true }, ( response ) => { console.log( response ); window.location="/qna" } )
});

/**************************************
Set a callback for whenthe window loads
**************************************/
window.onload = () => {
    if( sessionStorage.getItem( "room_id" ) != null )
        {
        socket.emit( 'JOIN ROOM', { room_id: sessionStorage.getItem( "room_id" ) }, ( response ) => { console.log( response ) } );
        document.getElementById('join-code').value = sessionStorage.getItem( "room_id" );

        const type_button = document.getElementById( 'player-type' );
        const quest_button = document.getElementById( 'question-button' );
        type_button.style.display = "none";
        quest_button.style.display = "none";
        }
};

window.onbeforeunload = () => {
    var cond1 = window.performance.getEntriesByType( 'navigation' )[0].type == 'reload';
    var cond2 = Boolean( sessionStorage.getItem( "linkClicked" ) == "true" );
    if( cond2 )
        {
        const waitingRoomList = document.getElementById('waiting-room-list');
        sessionStorage.removeItem( "room_id" );
        waitingRoomList.innerHTML = '';
        document.getElementById('join-code').value = '';
        }
    sessionStorage.setItem( "linkClicked", false );

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

    