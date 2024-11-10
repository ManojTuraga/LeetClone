// Show the Start button after 19 seconds
setTimeout(() => {
    document.getElementById('start-btn').style.display = 'block';
    document.getElementById('start-btn').style.animation = 'fadeInAnimation ease 3s';
}, 17000);


document.getElementById( 'start-btn' ).addEventListener('click', () => {
    window.location = "/questions";
  });