document.getElementById('toggle-btn').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    const headerContent = document.querySelector('.header');
    const authButtonContent = document.querySelector( '.auth-buttons' );

    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('collapsed');
    headerContent.classList.toggle( 'collapsed' );
    authButtonContent.classList.toggle( 'collapsed' );

    // sidebar collapse arrow
    if (sidebar.classList.contains('collapsed')) {
        this.innerHTML = '&#x25B6;'; // up
    } else {
        this.innerHTML = '&#x25C0;'; //down
    }
});
