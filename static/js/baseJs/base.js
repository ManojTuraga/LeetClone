/******************************************************************************
Module: base.js
Creation Date: Novemeber 20th, 2024
Author: Connor Forristal
Contributors:

Description:
   This page handles the basic logic that all inherting page will use, including
   the behavior of the navigation bar

Inputs:
    User Interaction on the page

Outputs:
    Web Page state change

Preconditions:
    The navigation button and navigation ar must exist as elements on the page

Postconditions:
    The nav bar is either visible or collapsed

Error Conditions:
    None

Side Effects:
    None

Invariants
    None

Known Faults

Sources: W3Schools
******************************************************************************/
/*
Utilized JavaScript from w3schools
https://www.w3schools.com/howto/howto_js_collapse_sidebar.asp
*/

// This function is responsible for opening the nav bar
function openNav() {
    // set the size of the nav bar
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main-cols").style.marginLeft = "250px";
    document.getElementById("leetclone-title").style.marginLeft = "250px";

    // Change the onclick attribute so that clicking it will close the
    // nav bar
    document.getElementById("sidebar-btn").setAttribute("onclick", "closeNav()");
  }
  
// This function is responsible for closing the nav bar
function closeNav() {
  // Set the size of the nav bar
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main-cols").style.marginLeft= "0";
  document.getElementById("leetclone-title").style.marginLeft = "0";

  // Make it so that clicking the button will open the nav bar
  const sidebar_btn = document.getElementById("sidebar-btn")
  sidebar_btn.setAttribute("onclick", "openNav()");
  sidebar_btn.blur();
}