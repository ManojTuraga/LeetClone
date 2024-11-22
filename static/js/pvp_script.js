var socket = io({ closeOnBeforeunload: false});

socket.on( "room_count", (...args) => { console.log( args ) } );
socket.on( "test_reload_out", (...args) => { window.location="/home" } );

window.onload = () => {
    socket.emit( 'JOIN ROOM', { room_id: "test_room" }, (response) => { console.log(response) } );
}

window.onbeforeunload = () => {
    socket.emit( 'test_reload', { room_id: "test_room" }, (response) => { console.log(response) } );
    setTimeout(() => {}, 10000);
}

window.pagehide = () =>
    {
    socket.close();
    }