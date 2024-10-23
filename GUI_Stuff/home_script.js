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
