// Personal Brand Website - Harikrishnan N
// JavaScript Module Structure

// Intersection Observer for scroll animations
const ScrollAnimations = {
  init() {
    // Check if IntersectionObserver is supported
    if (!('IntersectionObserver' in window)) {
      // Fallback: add 'visible' class to all fade-in elements immediately
      document.querySelectorAll('.fade-in').forEach(el => {
        el.classList.add('visible');
      });
      return;
    }

    // Create IntersectionObserver instance with threshold configuration
    const observerOptions = {
      root: null, // Use viewport as root
      rootMargin: '0px',
      threshold: 0.1 // Trigger when 10% of element is visible
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        // Add 'visible' class when element enters viewport
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          // Optional: stop observing after animation triggers once
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe all elements with .fade-in class
    this.observeElements(observer);
  },
  
  observeElements(observer) {
    // Select all elements with .fade-in class
    const fadeInElements = document.querySelectorAll('.fade-in');
    
    // Observe each element
    fadeInElements.forEach(element => {
      observer.observe(element);
    });
  }
};

// Smooth scroll navigation
const Navigation = {
  init() {
    // Select all anchor elements with href starting with #
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    // Attach click event handlers to each navigation link
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        // Prevent default anchor behavior
        e.preventDefault();
        
        // Get the target section ID from href
        const targetId = link.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        
        // Scroll to target section if it exists
        if (targetSection) {
          this.scrollToSection(targetSection);
        }
      });
    });
  },
  
  scrollToSection(target) {
    // Implement smooth scroll to target section using scrollIntoView
    // Set scroll behavior to 'smooth' with 0.8s timing (handled by CSS scroll-behavior)
    target.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
};

// Stat card number animations
const StatAnimations = {
  init() {
    const statValues = document.querySelectorAll('.stat-card__value[data-target]');

    if (statValues.length === 0) {
      return;
    }

    // Fallback: animate immediately if IntersectionObserver is unavailable
    if (!('IntersectionObserver' in window)) {
      statValues.forEach((valueElement) => {
        const target = parseInt(valueElement.dataset.target || '0', 10);

        if (Number.isFinite(target) && target > 0) {
          this.animateValue(valueElement, target, 1500);
          valueElement.dataset.animated = 'true';
        }
      });
      return;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        const valueElement = entry.target;
        const alreadyAnimated = valueElement.dataset.animated === 'true';
        const target = parseInt(valueElement.dataset.target || '0', 10);

        if (!alreadyAnimated && Number.isFinite(target) && target > 0) {
          this.animateValue(valueElement, target, 1500);
          valueElement.dataset.animated = 'true';
        }

        observer.unobserve(valueElement);
      });
    }, {
      root: null,
      rootMargin: '0px',
      threshold: 0.35
    });

    statValues.forEach((valueElement) => {
      observer.observe(valueElement);
    });
  },

  easeOutQuad(progress) {
    return progress * (2 - progress);
  },

  animateValue(element, target, duration) {
    const start = 0;
    const startTime = performance.now();

    const tick = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = this.easeOutQuad(progress);
      const currentValue = Math.round(start + (target - start) * easedProgress);

      element.textContent = currentValue.toString();

      if (progress < 1) {
        requestAnimationFrame(tick);
      } else {
        element.textContent = target.toString();
      }
    };

    requestAnimationFrame(tick);
  }
};

// Initialize all modules on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  ScrollAnimations.init();
  Navigation.init();
  StatAnimations.init();
});
