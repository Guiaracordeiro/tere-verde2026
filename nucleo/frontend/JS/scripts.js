
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tab-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    var tabToShow = document.getElementById(tabName);
    if (tabToShow) {
        tabToShow.style.display = "block";
    }

    if (evt && evt.currentTarget) {
        evt.currentTarget.className += " active";
    }
}

document.addEventListener('DOMContentLoaded', function() {
 
    var firstTabButton = document.querySelector(".tab-link");
    
    if (firstTabButton) {
        firstTabButton.click();
    }
});
