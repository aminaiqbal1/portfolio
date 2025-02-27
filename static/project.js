document.addEventListener("DOMContentLoaded", () => {
    // Register ScrollTrigger plugin
    gsap.registerPlugin(ScrollTrigger);
  
    // Animate Section Title
    gsap.to(".section-title", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: { trigger: ".section-title", start: "top 80%" }
    });
  
    // Animate each project card
    gsap.utils.toArray(".project-card").forEach(card => {
      gsap.to(card, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out",
        scrollTrigger: {
          trigger: card,
          start: "top 80%",
          toggleActions: "play none none reverse"
        }
      });
    });
  
    // Animate Call-to-Action Section
    gsap.to(".cta-section", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: { trigger: ".cta-section", start: "top 80%" }
    });
  });
  