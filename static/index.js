'use strict';



/**
 * add event listener on multiple elements
 */

const addEventOnElements = function (elements, eventType, callback) {
  for (let i = 0, len = elements.length; i < len; i++) {
    elements[i].addEventListener(eventType, callback);
  }
}



/**
 * PRELOADER
 * 
 * preloader will be visible until document load
 */

const preloader = document.querySelector("[data-preloader]");

window.addEventListener("load", function () {
  preloader.classList.add("loaded");
  document.body.classList.add("loaded");
});



/**
 * MOBILE NAVBAR
 * 
 * show the mobile navbar when click menu button
 * and hidden after click menu close button or overlay
 */

const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");
const overlay = document.querySelector("[data-overlay]");

const toggleNav = function () {
  navbar.classList.toggle("active");
  overlay.classList.toggle("active");
  document.body.classList.toggle("nav-active");
}

addEventOnElements(navTogglers, "click", toggleNav);



/**
 * HEADER & BACK TOP BTN
 * 
 * active header & back top btn when window scroll down to 100px
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

const activeElementOnScroll = function () {
  if (window.scrollY > 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
}

window.addEventListener("scroll", activeElementOnScroll);



/**
 * SCROLL REVEAL
 */

const revealElements = document.querySelectorAll("[data-reveal]");

const revealElementOnScroll = function () {
  for (let i = 0, len = revealElements.length; i < len; i++) {
    if (revealElements[i].getBoundingClientRect().top < window.innerHeight / 1.15) {
      revealElements[i].classList.add("revealed");
    } else {
      revealElements[i].classList.remove("revealed");
    }
  }
}

window.addEventListener("scroll", revealElementOnScroll);

window.addEventListener("load", revealElementOnScroll);


// Fonction pour remplacer les termes par "symptômes"
document.getElementById('symptomes-btn').addEventListener('click', () => {
  document.getElementById('symptomes-btn').classList.add('active')
  document.getElementById('facteur-btn').classList.remove('active')
  document.getElementById('prevention-btn').classList.remove('active')
  let aboutChange = document.getElementById('about-change');
  let html = aboutChange.innerHTML;

  // Remplacements des termes spécifiés
  html = html.replace(/facteurs de risque|outils de prévention/g, "symptômes");
  html = html.replace(/Mauvaise alimentation|Faire du sport/g, "Une soif excessive");
  html = html.replace(/L'obésité|Alimentation equilibré/g, "Des urines fréquentes");
  html = html.replace("Les antécédents familiaux", "Fatigue excessive");
  html = html.replace("Gestion du stress", "Fatigue excessive");
  html = html.replace(/Hypertension artérielle|Arrêter de fumer/g, "Perte de poids");

  aboutChange.innerHTML = html; // Met à jour le contenu HTML avec les modifications
});

// Fonction pour remplacer les termes par "facteurs de risque"
document.getElementById('facteur-btn').addEventListener('click', () => {

  document.getElementById('symptomes-btn').classList.remove('active')
  document.getElementById('facteur-btn').classList.add('active')
  document.getElementById('prevention-btn').classList.remove('active')

  let aboutChange = document.getElementById('about-change');
  let html = aboutChange.innerHTML;

  // Remplacements des termes spécifiés
  html = html.replace(/symptômes|outils de prévention/g, "facteurs de risque");
  html = html.replace(/Une soif excessive|Faire du sport/g, "Mauvaise alimentation");
  html = html.replace(/Des urines fréquentes|Alimentation equilibré/g, "L'obésité");
  html = html.replace("Fatigue excessive", "Les antécédents familiaux");
  html = html.replace("Gestion du stress", "Les antécédents familiaux");
  html = html.replace(/Perte de poids|Arrêter de fumer/g, "Hypertension artérielle");

  aboutChange.innerHTML = html; // Met à jour le contenu HTML avec les modifications
});

// Fonction pour remplacer les termes par "outils de prévention"
document.getElementById("prevention-btn").addEventListener('click', () => {
  document.getElementById('symptomes-btn').classList.remove('active')
  document.getElementById('facteur-btn').classList.remove('active')
  document.getElementById('prevention-btn').classList.add('active')
  let aboutChange = document.getElementById('about-change');
  let html = aboutChange.innerHTML;

  // Remplacements des termes spécifiés
  html = html.replace(/facteurs de risque|symptômes/g, "outils de prévention");
  html = html.replace(/Mauvaise alimentation|Une soif excessive/g, "Faire du sport");
  html = html.replace(/L'obésité|Des urines fréquentes/g, "Alimentation equilibré");
  html = html.replace(/Les antécédents familiaux|Fatigue excessive/g, "Gestion du stress");
  html = html.replace(/Hypertension artérielle|Perte de poids/g, "Arrêter de fumer");

  aboutChange.innerHTML = html; // Met à jour le contenu HTML avec les modifications
});

// Select all buttons with the class 'btn-text title-lg'
var btn1 = document.getElementById('a-href1');

    btn1.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action of the link

        // Show the popup container
        var popupContainer = document.getElementById('popupContainer1');
        popupContainer.style.display = 'flex';

        // Blur the body
        document.body.classList.add('active_blur');
    });
    

var btn2 = document.getElementById('a-href2');
btn2.addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default action of the link

  // Show the popup container
  var popupContainer = document.getElementById('popupContainer2');
  popupContainer.style.display = 'flex';

  // Blur the body
  document.body.classList.add('active_blur');
});

var btn3 = document.getElementById('a-href3');
btn3.addEventListener('click', function(event) {
  event.preventDefault(); // Prevent the default action of the link

  // Show the popup container
  var popupContainer = document.getElementById('popupContainer3');
  popupContainer.style.display = 'flex';

  // Blur the body
  document.body.classList.add('active_blur');
});

// Function to close the popup and remove the blur effect
function closePopup(id) {
    var popupContainer = document.getElementById('popupContainer'+id);
    popupContainer.style.display = 'none';

    // Remove the blur effect from the body
    document.body.classList.remove('active_blur');
}
