/* BH Door Solutions — minimal progressive-enhancement JS */
(function () {
  "use strict";
  var header = document.getElementById("siteHeader");
  var toggle = document.getElementById("navToggle");

  // Sticky header shadow on scroll
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Mobile menu toggle
  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Dropdown toggles (mobile / keyboard)
  var ddButtons = document.querySelectorAll(".nav-menu .has-dd > button");
  ddButtons.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      // Only intercept as an accordion on mobile widths
      if (window.matchMedia("(max-width: 860px)").matches) {
        e.preventDefault();
        var li = btn.parentElement;
        var isOpen = li.classList.toggle("open");
        btn.setAttribute("aria-expanded", isOpen ? "true" : "false");
      }
    });
  });

  // Close mobile menu when a link is tapped
  document.querySelectorAll(".nav-menu a").forEach(function (a) {
    a.addEventListener("click", function () {
      header && header.classList.remove("menu-open");
      toggle && toggle.setAttribute("aria-expanded", "false");
    });
  });

  // Close menu on Escape
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && header) {
      header.classList.remove("menu-open");
      document.querySelectorAll(".nav-menu .has-dd.open").forEach(function (li) {
        li.classList.remove("open");
      });
    }
  });
})();
