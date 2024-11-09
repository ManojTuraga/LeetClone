// Show the Start button after 19 seconds
setTimeout(() => {
    document.getElementById('start-btn').style.display = 'block';
}, 16000);

document.getElementById( 'start-btn' ).addEventListener('click', () => {
    window.location = "/questions";
  });