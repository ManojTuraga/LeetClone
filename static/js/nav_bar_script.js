/******************************************************************************
Module: nav_bar_script.js
Creation Date: October 22th, 2024
Author: Clare Channel
Contributors: Clare Channel, Manoj Turaga

Description:
    This module will contain callbacks for elements that are on the navigation/
    side bar on the base page. The result of these callbacks being triggered
    is a modification on the state of the page.

Inputs:
    User Input

Outputs:
    None

Preconditions:
    The user clicks the toggle button on the navigation bar

Postconditions:
    The resulting web page is either minimzied or expanded based on the previous
    state

Error Conditions:
    None

Side Effects:
    None

Invariants
    The 'toggle-button' element must exist on the page

Known Faults

Sources: W3Schools
******************************************************************************/

/**************************************
Create a callback on the toggle-btn on
the sidebar of the base page. Clicking
the toggle button wiil either minimize
the sidebar or expand it
**************************************/
document.getElementById('toggle-btn').addEventListener('click', function() {
    /**************************************
    Get the sidebar, main-content, header, 
    and auth-buttons from the page. These 
    will be the elements that we will 
    trigger the collapse on 
    **************************************/
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    const headerContent = document.querySelector('.header');
    const authButtonContent = document.querySelector( '.auth-buttons' );

    /**************************************
    Toggle the collapse behavior on the 
    elements previously obtained
    **************************************/
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('collapsed');
    headerContent.classList.toggle( 'collapsed' );
    authButtonContent.classList.toggle( 'collapsed' );

    /**************************************
    Change the display of the toggle button
    arrow 
    **************************************/
    if (sidebar.classList.contains('collapsed')) {
        this.innerHTML = '&#x25B6;'; // left facing arrow
    } else {
        this.innerHTML = '&#x25C0;'; // right facing arrow
    }
});
