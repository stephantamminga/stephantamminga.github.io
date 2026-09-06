/* Fotoclub Beeldspraak - mobile navigation toggle & image lightbox
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

  /* ============================================================= */
  /* Image Lightbox / Modal                                        */
  /* ============================================================= */

  var modal = document.getElementById("imageModal");
  var modalOverlay = document.getElementById("modalOverlay");
  var modalImage = document.getElementById("modalImage");
  var modalCaption = document.getElementById("modalCaption");
  var modalClose = document.getElementById("modalClose");
  var modalPrev = document.getElementById("modalPrev");
  var modalNext = document.getElementById("modalNext");

  var currentImages = [];
  var currentIndex = -1;

  function openModal(index) {
    currentIndex = index;
    updateModalContent();
    modal.classList.add("visible");
    modalOverlay.classList.add("visible");
    document.body.style.overflow = "hidden";
    updateNavButtons();
  }

  function closeModal() {
    modal.classList.remove("visible");
    modalOverlay.classList.remove("visible");
    document.body.style.overflow = "";
  }

  function updateModalContent() {
    if (currentIndex >= 0 && currentIndex < currentImages.length) {
      var imgData = currentImages[currentIndex];
      modalImage.src = imgData.src;
      modalImage.alt = imgData.alt || "";
      modalCaption.textContent = imgData.caption || "";
    }
  }

  function updateNavButtons() {
    if (currentImages.length <= 1) {
      modalPrev.disabled = true;
      modalNext.disabled = true;
      modalPrev.style.display = "none";
      modalNext.style.display = "none";
      return;
    }
    modalPrev.disabled = currentIndex <= 0;
    modalNext.disabled = currentIndex >= currentImages.length - 1;
    modalPrev.style.display = "flex";
    modalNext.style.display = "flex";
  }

  function navPrev() {
    if (currentIndex > 0) {
      openModal(currentIndex - 1);
    }
  }

  function navNext() {
    if (currentIndex < currentImages.length - 1) {
      openModal(currentIndex + 1);
    }
  }

  function handleKeyDown(e) {
    if (!modal.classList.contains("visible")) return;
    switch (e.key) {
      case "Escape": closeModal(); break;
      case "ArrowLeft": navPrev(); break;
      case "ArrowRight": navNext(); break;
    }
  }

  /* Collect all images from the content area */
  function collectPageImages() {
    var contentEl = document.getElementById("content");
    if (!contentEl) return [];

    var images = [];
    var imgElements = contentEl.querySelectorAll("img");
    
    imgElements.forEach(function (img) {
      images.push({
        src: img.src,
        alt: img.alt,
        caption: getCaptionForImage(img)
      });
    });
    
    return images;
  }

  /* Get caption from the next sibling if it's a caption element */
  function getCaptionForImage(img) {
    var next = img.nextElementSibling;
    if (next && (next.classList.contains("photo-caption") || 
                  next.classList.contains("caption") ||
                  (next.tagName === "DIV" && next.textContent.trim().length > 0))) {
      return next.textContent.trim();
    }
    return img.alt || "";
  }

  /* Initialize image click handlers */
  function initImageLightbox() {
    var contentEl = document.getElementById("content");
    if (!contentEl) return;

    var imgElements = contentEl.querySelectorAll("img");
    currentImages = collectPageImages();

    if (currentImages.length === 0) return;

    imgElements.forEach(function (img, index) {
      img.style.cursor = "pointer";
      img.addEventListener("click", function (e) {
        e.preventDefault();
        openModal(index);
      });
    });

    /* Modal event listeners */
    modalClose.addEventListener("click", closeModal);
    modalOverlay.addEventListener("click", closeModal);
    modalPrev.addEventListener("click", navPrev);
    modalNext.addEventListener("click", navNext);
    modalImage.addEventListener("click", navNext);
    document.addEventListener("keydown", handleKeyDown);
  }

  /* Initialize on page load */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initImageLightbox);
  } else {
    initImageLightbox();
  }

})();
