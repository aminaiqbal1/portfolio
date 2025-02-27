document.addEventListener("DOMContentLoaded", () => {
    // Register GSAP ScrollTrigger plugin
    gsap.registerPlugin(ScrollTrigger);
  
    // Animate header section
    gsap.to(".header", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: { trigger: ".header", start: "top 90%" }
    });
  
    // Animate each skill card on scroll
    gsap.utils.toArray(".skill-card").forEach(card => {
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
  
    // Animate testimonials section
    gsap.to(".testimonials", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: { trigger: ".testimonials", start: "top 80%" }
    });
    gsap.utils.toArray(".testimonial-card").forEach(card => {
      gsap.to(card, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out",
        scrollTrigger: {
          trigger: card,
          start: "top 85%",
          toggleActions: "play none none reverse"
        }
      });
    });
  
    // Animate call-to-action section
    gsap.to(".cta", {
      opacity: 1,
      y: 0,
      duration: 1,
      ease: "power3.out",
      scrollTrigger: { trigger: ".cta", start: "top 80%" }
    });
  });
  