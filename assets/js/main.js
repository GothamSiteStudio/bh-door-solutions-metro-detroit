/* BH Door Solutions — progressive-enhancement JS (accessibility-focused) */
(function () {
  "use strict";
  var header = document.getElementById("siteHeader");
  var toggle = document.getElementById("navToggle");
  var isMobile = function () { return window.matchMedia("(max-width: 860px)").matches; };

  /* Sticky header shadow on scroll */
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 8); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* Mobile menu toggle */
  if (toggle && header) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("menu-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  /* Accessible dropdown disclosures (Services / Service Areas) */
  var items = Array.prototype.slice.call(document.querySelectorAll(".nav-menu .has-dd"));
  items.forEach(function (li) {
    var btn = li.querySelector(":scope > button");
    if (!btn) return;

    // Keep aria-expanded in sync with the actual open state (hover, focus, or click).
    var sync = function () {
      var open = li.classList.contains("open") || li.matches(":focus-within") || li.matches(":hover");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    };

    // Click toggles the accordion on mobile; on desktop hover/focus handles reveal
    btn.addEventListener("click", function (e) {
      if (isMobile()) {
        e.preventDefault();
        li.classList.toggle("open");
        sync();
      }
    });

    li.addEventListener("mouseenter", sync);
    li.addEventListener("mouseleave", function () { sync(); });
    // Reveal on keyboard focus (belt-and-suspenders alongside CSS :focus-within)
    li.addEventListener("focusin", function () { li.classList.add("open"); sync(); });

    // When focus leaves the whole item, close and reset
    li.addEventListener("focusout", function (e) {
      if (!li.contains(e.relatedTarget)) {
        li.classList.remove("open");
        sync();
      }
    });

    // Escape closes the dropdown and returns focus to its button
    li.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && (li.classList.contains("open") || li.matches(":focus-within"))) {
        li.classList.remove("open");
        btn.focus();
        sync();
      }
      // Arrow Down opens and moves focus to the first item
      if (e.key === "ArrowDown" && e.target === btn) {
        e.preventDefault();
        li.classList.add("open");
        sync();
        var first = li.querySelector(".dropdown a");
        if (first) first.focus();
      }
    });
  });

  /* Close the mobile menu when a nav link is activated */
  document.querySelectorAll(".nav-menu a").forEach(function (a) {
    a.addEventListener("click", function () {
      if (header) header.classList.remove("menu-open");
      if (toggle) {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
      }
    });
  });

  /* Global Escape: close the mobile menu */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && header && header.classList.contains("menu-open")) {
      header.classList.remove("menu-open");
      if (toggle) {
        toggle.setAttribute("aria-expanded", "false");
        toggle.setAttribute("aria-label", "Open menu");
        toggle.focus();
      }
    }
  });
})();
