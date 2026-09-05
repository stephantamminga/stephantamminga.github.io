/* Fotoclub Beeldspraak - mobile navigation toggle
 * Works under file:// and on github.io */

(function () {
  "use strict";

  var navEl = document.getElementById("nav");
  var navToggle = document.getElementById("navToggle");
  var navOverlay = document.getElementById("navOverlay");

  function isMobile() {
    return window.matchMedia("(max-width: 800px)").matches;
  }

  function openNav() {
    navEl.classList.add("open");
    navOverlay.classList.add("visible");
    navToggle.setAttribute("aria-expanded", "true");
  }

  function closeNav() {
    navEl.classList.remove("open");
    navOverlay.classList.remove("visible");
    navToggle.setAttribute("aria-expanded", "false");
  }

  function toggleNav() {
    if (navEl.classList.contains("open")) { closeNav(); } else { openNav(); }
  }

  if (navToggle) { navToggle.addEventListener("click", toggleNav); }
  if (navOverlay) { navOverlay.addEventListener("click", closeNav); }

  /* Close the menu when a link is chosen (mobile UX) */
  var navLinks = document.querySelectorAll(".nav a");
  navLinks.forEach(function (a) {
    a.addEventListener("click", function () { 
      if (isMobile()) { closeNav(); }
    });
  });

  /* Close the menu if the viewport grows to desktop */
  window.addEventListener("resize", function () {
    if (!isMobile()) { closeNav(); }
  });
})();
