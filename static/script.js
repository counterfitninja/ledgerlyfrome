/* Ledgerly — client-side interactivity only (content rendered server-side) */

/* ── FAQ Accordion ───────────────────────────────────────────────────────── */
document.querySelectorAll(".faq-item__q").forEach(btn => {
  btn.addEventListener("click", () => {
    const item   = btn.closest(".faq-item");
    const isOpen = item.classList.contains("open");
    document.querySelectorAll(".faq-item").forEach(i => {
      i.classList.remove("open");
      i.querySelector(".faq-item__q").setAttribute("aria-expanded", "false");
    });
    if (!isOpen) {
      item.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
    }
  });
});

/* ── Mobile hamburger ────────────────────────────────────────────────────── */
const hamburger  = document.getElementById("hamburger");
const mobileMenu = document.getElementById("mobile-menu");
if (hamburger && mobileMenu) {
  hamburger.addEventListener("click", () => {
    const open = mobileMenu.classList.toggle("open");
    hamburger.setAttribute("aria-expanded", open);
  });
  mobileMenu.addEventListener("click", e => {
    if (e.target.tagName === "A") {
      mobileMenu.classList.remove("open");
      hamburger.setAttribute("aria-expanded", "false");
    }
  });
}

/* ── Sticky nav shadow ───────────────────────────────────────────────────── */
const nav = document.getElementById("nav");
if (nav) {
  window.addEventListener("scroll", () => {
    nav.style.boxShadow = window.scrollY > 10
      ? "0 4px 20px rgba(13,148,136,.15)"
      : "";
  }, { passive: true });
}
