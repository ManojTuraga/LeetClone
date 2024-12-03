/*
Utilized JavaScript from w3schools
https://www.w3schools.com/howto/howto_js_collapse_sidebar.asp
*/

function openNav() {
    document.getElementById("mySidebar").style.width = "250px";
    document.getElementById("main-cols").style.marginLeft = "250px";
    document.getElementById("leetclone-title").style.marginLeft = "250px";
    document.getElementById("sidebar-btn").setAttribute("onclick", "closeNav()");
  }
  
function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main-cols").style.marginLeft= "0";
  document.getElementById("leetclone-title").style.marginLeft = "0";

  const sidebar_btn = document.getElementById("sidebar-btn")
  sidebar_btn.setAttribute("onclick", "openNav()");
  sidebar_btn.blur();
}