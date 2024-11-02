document.getElementById('toggle-btn').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');

    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('collapsed');

    // sidebar collapse arrow
    if (sidebar.classList.contains('collapsed')) {
        this.innerHTML = '&#x25BC;'; //down
    } else {
        this.innerHTML = '&#x25B2;'; // up
    }
});

// Show the Start button after 19 seconds
setTimeout(() => {
    document.getElementById('start-btn').style.display = 'block';
}, 16000);

// Open sidebar when Start button is clicked
document.getElementById('start-btn').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.remove('collapsed'); // Ensure sidebar is visible
});

