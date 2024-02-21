/*!
    * Start Bootstrap - SB Admin v7.0.4 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2021 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

    /*
    //Get the button
    let mybutton = document.getElementById("btn-back-to-top");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
      scrollFunction();
    };

    function scrollFunction() {
      if (
        document.body.scrollTop > 20 ||
        document.documentElement.scrollTop > 20
      ) {
        mybutton.style.display = "block";
      } else {
        mybutton.style.display = "none";
      }
    }
    // When the user clicks on the button, scroll to the top of the document
    mybutton.addEventListener("click", backToTop);

    function backToTop() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }
    */

});


$(document).ready(function () {

  var element = document.body;
  var InitialFontSize = 0.875;
  var Divider = 16 // 16px = 1rem
  var Increment = 0.05 // 16px = 1rem
  var bodyFontSize = parseFloat(window.getComputedStyle(document.body, null).fontSize, 0);
  var fontSize = parseFloat(bodyFontSize / Divider);

  if(sessionStorage.getItem('font-size')){
    fontSize = sessionStorage.getItem('font-size');
  } else {
    sessionStorage.setItem('font-size', fontSize);
  }

  console.log(sessionStorage.getItem('font-size'));
  console.log(fontSize);
  document.body.style.fontSize = fontSize + 'rem';

  $('#increase, #decrease').on('click', function () { // click to increase or decrease
      var btn = $(this);
      // fontSize = parseFloat(sessionStorage.getItem('font-size'));
      // var fontSize = parseInt(window.getComputedStyle(document.body, null).fontSize, 0); // parse the body font size as a number

      if (btn[0].id === "increase") { // detect the button being clicked
          fontSize = fontSize + Increment; // increase the base font size
      } else {
          fontSize = fontSize - Increment; // or decrease
      }
      console.log(sessionStorage.getItem('font-size'));
      sessionStorage.setItem('font-size', fontSize);
      document.body.style.fontSize = fontSize + 'rem'; // set the body font size to the new value
  });
  $('#reset').on('click', function () { // click to increase or decrease
      fontSize = InitialFontSize;
      sessionStorage.setItem('font-size', fontSize);
      document.body.style.fontSize = InitialFontSize + 'rem'; // set the body font size to the new value
  });

  $('#highcontrast').on('click', function () {
        var element = document.body;
        if(sessionStorage.getItem('hc')){
            element.classList.remove("high-contrast");
            sessionStorage.removeItem('hc');
        } else {
            element.classList.add("high-contrast");
            sessionStorage.setItem('hc', 'Ok');
        }
    });

    // console.log(sessionStorage.getItem('hc'));
    if(sessionStorage.getItem('hc')){
        element.classList.add("high-contrast");
    } else {
        element.classList.remove("high-contrast");
    }

});

// function highcontrast() {
//   var element = document.body;
//   element.classList.toggle("high-contrast");
// }