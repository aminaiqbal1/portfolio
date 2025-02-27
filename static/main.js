document.addEventListener("DOMContentLoaded", () => {
    // Hero section animations
    gsap.from(".hero-text h1", { duration: 1.5, x: -50, opacity: 0, ease: "power3.out" });
    gsap.from(".hero-text h2", { duration: 1.2, x: -50, opacity: 0, delay: 0.5, ease: "power3.out" });
    gsap.from(".btn", { duration: 1, x: -50, opacity: 0, delay: 0.7, ease: "power3.out" });
    gsap.from(".hero-image img", { duration: 1.5, x: 50, opacity: 0, ease: "power3.out" });
    
    // Typed.js effect for dynamic text in hero section
    const typed = new Typed("#typed-text", {
      strings: ["Software Engineer", "Python Expert", "AI Developer"],
      typeSpeed: 50,
      backSpeed: 50,
      loop: true
    });
  
    // Button hover effects
    document.querySelectorAll(".btn").forEach(button => {
      button.addEventListener("mouseenter", () => {
        gsap.to(button, { scale: 1.1, duration: 0.3 });
      });
      button.addEventListener("mouseleave", () => {
        gsap.to(button, { scale: 1, duration: 0.3 });
      });
    });
  
    // Skills Section scroll animations using ScrollTrigger
    gsap.from("#skills h2", {
      scrollTrigger: {
        trigger: "#skills h2",
        start: "top 80%"
      },
      opacity: 0,
      y: 20,
      duration: 1,
      ease: "power3.out"
    });
    gsap.from("#skills li", {
      scrollTrigger: {
        trigger: "#skills li",
        start: "top 85%"
      },
      opacity: 0,
      y: 20,
      duration: 0.8,
      ease: "power3.out",
      stagger: 0.2
    });
  
    // Projects Section scroll animations using ScrollTrigger
    gsap.from("#projects h2", {
      scrollTrigger: {
        trigger: "#projects h2",
        start: "top 80%"
      },
      opacity: 0,
      y: 20,
      duration: 1,
      ease: "power3.out"
    });
    gsap.utils.toArray(".project-card").forEach(card => {
      gsap.from(card, {
        scrollTrigger: {
          trigger: card,
          start: "top 80%",
        },
        opacity: 0,
        y: 50,
        duration: 1,
        ease: "power3.out"
      });
    });
  
    // Navigation links smooth scroll (using jQuery for convenience)
    
      
});

  