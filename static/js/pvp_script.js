var socket;

window.onload = () => {
    socket = io();
    socket.emit( 'JOIN ROOM', { room_id: "test_room" }, (response) => { console.log(response); location.reload() } );
}

window.pagehide = () =>
    {
    socket.close();
    }