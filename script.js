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

// Form handling
const ContactForm = {
  init() {
    this.form = document.querySelector('.contact-form');
    this.successMessage = document.getElementById('form-success-message');
    this.globalError = document.getElementById('form-global-error');

    if (!this.form) {
      return;
    }

    const fields = this.form.querySelectorAll('input[name="name"], input[name="email"], textarea[name="message"]');
    fields.forEach((field) => {
      field.addEventListener('input', () => {
        this.clearFieldError(field);
        this.clearGlobalError();
      });
    });

    this.form.addEventListener('submit', async (event) => {
      event.preventDefault();
      this.clearGlobalError();

      const formData = new FormData(this.form);
      const validation = this.validate({
        name: (formData.get('name') || '').toString().trim(),
        email: (formData.get('email') || '').toString().trim(),
        message: (formData.get('message') || '').toString().trim()
      });

      if (!validation.valid) {
        this.renderValidationErrors(validation.errors);
        return;
      }

      try {
        const response = await fetch('/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams(formData).toString()
        });

        if (!response.ok) {
          throw new Error(`Submission failed with status ${response.status}`);
        }

        this.form.reset();
        this.clearAllErrors();
        this.showSuccess();
      } catch (error) {
        this.showGlobalError();
      }
    });
  },

  validate(data) {
    const errors = {};
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!data.name) {
      errors.name = 'Name is required.';
    }

    if (!data.email) {
      errors.email = 'Email is required.';
    } else if (!emailPattern.test(data.email)) {
      errors.email = 'Please enter a valid email address.';
    }

    if (!data.message) {
      errors.message = 'Message is required.';
    } else if (data.message.length < 10) {
      errors.message = 'Message must be at least 10 characters.';
    }

    return {
      valid: Object.keys(errors).length === 0,
      errors
    };
  },

  renderValidationErrors(errors) {
    this.clearAllErrors();

    Object.entries(errors).forEach(([fieldName, message]) => {
      const field = this.form.querySelector(`[name="${fieldName}"]`);
      const errorElement = document.getElementById(`${fieldName}-error`);

      if (field && errorElement) {
        field.classList.add('input-error');
        field.setAttribute('aria-invalid', 'true');
        errorElement.textContent = message;
        errorElement.hidden = false;
      }
    });
  },

  clearFieldError(field) {
    field.classList.remove('input-error');
    field.setAttribute('aria-invalid', 'false');

    const errorElement = document.getElementById(`${field.name}-error`);
    if (errorElement) {
      errorElement.textContent = '';
      errorElement.hidden = true;
    }
  },

  clearAllErrors() {
    const inputs = this.form.querySelectorAll('input[name="name"], input[name="email"], textarea[name="message"]');
    inputs.forEach((input) => this.clearFieldError(input));
    this.clearGlobalError();
  },

  showGlobalError() {
    if (!this.globalError) {
      return;
    }

    this.globalError.innerHTML = 'Unable to submit right now. Please email directly at <a href="mailto:harikrishnanz98@gmail.com">harikrishnanz98@gmail.com</a>.';
    this.globalError.hidden = false;
  },

  clearGlobalError() {
    if (!this.globalError) {
      return;
    }

    this.globalError.textContent = '';
    this.globalError.hidden = true;
  },

  showSuccess() {
    if (!this.successMessage) {
      return;
    }

    this.successMessage.hidden = false;

    window.setTimeout(() => {
      this.successMessage.hidden = true;
    }, 5000);
  }
};

// Initialize all modules on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  ScrollAnimations.init();
  Navigation.init();
  StatAnimations.init();
  ContactForm.init();
});
