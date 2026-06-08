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
      ? "0 10px 30px rgba(28, 54, 49, .08)"
      : "";
  }, { passive: true });
}

/* ── Hero no-copy state (for static page parity) ─────────────────────────── */
const heroInner = document.querySelector(".hero__inner");
const heroContent = document.querySelector(".hero__content");
if (heroInner && heroContent) {
  const heading = heroContent.querySelector("h1");
  const sub = heroContent.querySelector(".hero__sub");
  const headingText = heading ? heading.textContent.trim() : "";
  const subText = sub ? sub.textContent.trim() : "";

  if (!headingText && !subText) {
    heroInner.classList.add("hero__inner--no-copy");
    heroContent.style.display = "none";
  }
}

/* ── Reviews rail controls ───────────────────────────────────────────────── */
const reviewsTrack = document.getElementById("reviews-track");
const reviewControls = document.querySelectorAll("[data-review-scroll]");

if (reviewsTrack && reviewControls.length) {
  reviewControls.forEach(button => {
    button.addEventListener("click", () => {
      const firstCard = reviewsTrack.querySelector(".review-card");
      const scrollAmount = firstCard
        ? firstCard.getBoundingClientRect().width + 24
        : 320;
      const direction = button.dataset.reviewScroll === "next" ? 1 : -1;

      reviewsTrack.scrollBy({
        left: scrollAmount * direction,
        behavior: "smooth",
      });
    });
  });
}
