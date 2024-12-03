/******************************************************************************
Module: home_script.js
Creation Date: Novemeber 9th, 2024
Author: Clare Channel
Contributors: Clare Channel, Manoj Turaga, Connor Forristal

Description:
   This module performs simple javascript for making a button appear 
   later in the load process of the webpage. Includes an event listener 
   to send someone to the next page based on a button click.

Inputs:
    None

Outputs:
    None

Preconditions:
    The user clicks the start button

Postconditions:
    A new page is now loaded.

Error Conditions:
    None

Side Effects:
    None

Invariants
    None

Known Faults

Sources: W3Schools
******************************************************************************/

/**************************************
Adds an event listener so when the button 
is clicked, it will send the user to 
another page.
**************************************/
document.getElementById( 'start-btn' ).addEventListener('click', () => {
    window.location = "/questions";
  });