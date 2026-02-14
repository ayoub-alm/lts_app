// GSAP Animations
document.addEventListener("DOMContentLoaded", (event) => {
  gsap.registerPlugin(ScrollTrigger);

  // Navbar Scroll Effect
  window.addEventListener('scroll', () => {
      const navbar = document.querySelector('.navbar');
      if (window.scrollY > 50) {
          navbar.style.boxShadow = "0 4px 6px -1px rgba(0, 0, 0, 0.1)";
          navbar.style.backgroundColor = "rgba(255, 255, 255, 0.95)";
      } else {
          navbar.style.boxShadow = "none";
          navbar.style.backgroundColor = "rgba(255, 255, 255, 0.8)";
      }
  });

  // Hero Animation
  gsap.from(".hero-title", {
      duration: 1,
      y: 50,
      opacity: 0,
      ease: "power3.out",
      delay: 0.2
  });

  gsap.from(".hero-subtitle", {
      duration: 1,
      y: 30,
      opacity: 0,
      ease: "power3.out",
      delay: 0.4
  });

  gsap.from(".btn-primary-custom, .btn-outline-secondary", {
      duration: 1,
      y: 20,
      opacity: 0,
      ease: "power3.out",
      delay: 0.6,
      stagger: 0.2
  });

  // Cards Animation (ScrollTrigger)
  const cards = gsap.utils.toArray('.formation-card');
  if (cards.length > 0) {
      gsap.from(cards, {
          scrollTrigger: {
              trigger: cards[0],
              start: "top 85%",
              toggleActions: "play none none reverse"
          },
          duration: 0.8,
          y: 50,
          opacity: 0,
          stagger: 0.2,
          ease: "power2.out"
      });
  }

  // Section Titles
  gsap.utils.toArray('.section-title').forEach(title => {
      gsap.from(title, {
          scrollTrigger: {
              trigger: title,
              start: "top 85%",
              toggleActions: "play none none reverse"
          },
          duration: 1,
          x: -50,
          opacity: 0,
          ease: "power3.out"
      });
  });
});
