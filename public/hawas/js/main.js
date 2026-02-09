/**
 * Hawas Website - Main JavaScript
 * hawasapp.com
 */

(function() {
  'use strict';

  // ============================================
  // LANGUAGE MANAGEMENT
  // ============================================

  const LANGUAGES = {
    en: {
      code: 'en',
      name: 'English',
      dir: 'ltr',
      toggle: 'العربية'
    },
    ar: {
      code: 'ar',
      name: 'العربية',
      dir: 'rtl',
      toggle: 'English'
    }
  };

  // Get current language from URL path or localStorage
  function getCurrentLanguage() {
    const path = window.location.pathname;
    if (path.includes('/ar/')) {
      return 'ar';
    }
    return localStorage.getItem('hawas-lang') || 'en';
  }

  // Set language preference
  function setLanguagePreference(lang) {
    localStorage.setItem('hawas-lang', lang);
  }

  // Get translated page URL
  function getTranslatedPageUrl(targetLang) {
    const currentPath = window.location.pathname;
    const currentLang = getCurrentLanguage();

    if (targetLang === 'ar') {
      if (currentPath === '/' || currentPath === '/index.html') {
        return '/ar/';
      }
      if (!currentPath.includes('/ar/')) {
        return '/ar' + currentPath;
      }
      return currentPath;
    } else {
      // Switch to English
      if (currentPath.includes('/ar/')) {
        const enPath = currentPath.replace('/ar/', '/').replace('/ar', '/');
        return enPath === '' ? '/' : enPath;
      }
      return currentPath;
    }
  }

  // Initialize language toggle
  function initLanguageToggle() {
    const toggles = document.querySelectorAll('.nav__lang-toggle, .footer__lang-toggle');
    const currentLang = getCurrentLanguage();
    const targetLang = currentLang === 'en' ? 'ar' : 'en';

    toggles.forEach(toggle => {
      toggle.textContent = LANGUAGES[targetLang].toggle;
      toggle.setAttribute('aria-label', `Switch to ${LANGUAGES[targetLang].name}`);

      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        setLanguagePreference(targetLang);
        window.location.href = getTranslatedPageUrl(targetLang);
      });
    });

    // Set document direction
    document.documentElement.setAttribute('dir', LANGUAGES[currentLang].dir);
    document.documentElement.setAttribute('lang', currentLang);
  }


  // ============================================
  // MOBILE NAVIGATION
  // ============================================

  function initMobileNav() {
    const nav = document.querySelector('.nav');
    const toggle = document.querySelector('.nav__mobile-toggle');

    if (!toggle) return;

    toggle.addEventListener('click', () => {
      nav.classList.toggle('nav--mobile-open');
      const isOpen = nav.classList.contains('nav--mobile-open');
      toggle.setAttribute('aria-expanded', isOpen);
      toggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
    });

    // Close mobile nav on link click
    const navLinks = document.querySelectorAll('.nav__link');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        nav.classList.remove('nav--mobile-open');
      });
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && nav.classList.contains('nav--mobile-open')) {
        nav.classList.remove('nav--mobile-open');
      }
    });
  }


  // ============================================
  // SCROLL ANIMATIONS
  // ============================================

  function initScrollAnimations() {
    const observerOptions = {
      root: null,
      rootMargin: '0px',
      threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fadeIn');
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    // Observe elements with data-animate attribute
    const animateElements = document.querySelectorAll('[data-animate]');
    animateElements.forEach(el => {
      el.style.opacity = '0';
      observer.observe(el);
    });
  }


  // ============================================
  // NAVBAR SCROLL BEHAVIOR
  // ============================================

  function initNavbarScroll() {
    const nav = document.querySelector('.nav');
    if (!nav) return;

    let lastScrollY = window.scrollY;
    let ticking = false;

    function updateNav() {
      const currentScrollY = window.scrollY;

      // Add shadow when scrolled
      if (currentScrollY > 10) {
        nav.style.boxShadow = 'var(--shadow-md)';
      } else {
        nav.style.boxShadow = 'none';
      }

      lastScrollY = currentScrollY;
      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(updateNav);
        ticking = true;
      }
    }, { passive: true });
  }


  // ============================================
  // SMOOTH SCROLL
  // ============================================

  function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
      link.addEventListener('click', (e) => {
        const targetId = link.getAttribute('href');
        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          const navHeight = document.querySelector('.nav')?.offsetHeight || 0;
          const targetPosition = targetElement.offsetTop - navHeight - 20;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  }


  // ============================================
  // COUNTER ANIMATION
  // ============================================

  function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = formatNumber(target);
        clearInterval(timer);
      } else {
        element.textContent = formatNumber(Math.floor(current));
      }
    }, 16);
  }

  function formatNumber(num) {
    if (num >= 1000) {
      return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K+';
    }
    return num.toString() + '+';
  }

  function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');
    if (counters.length === 0) return;

    const observerOptions = {
      threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const target = parseInt(entry.target.getAttribute('data-counter'), 10);
          animateCounter(entry.target, target);
          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    counters.forEach(counter => observer.observe(counter));
  }


  // ============================================
  // CURRENT YEAR
  // ============================================

  function setCurrentYear() {
    const yearElements = document.querySelectorAll('[data-year]');
    const currentYear = new Date().getFullYear();
    yearElements.forEach(el => {
      el.textContent = currentYear;
    });
  }


  // ============================================
  // ACCESSIBILITY ENHANCEMENTS
  // ============================================

  function initAccessibility() {
    // Skip to main content link
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
      skipLink.addEventListener('click', (e) => {
        e.preventDefault();
        const main = document.querySelector('main');
        if (main) {
          main.setAttribute('tabindex', '-1');
          main.focus();
        }
      });
    }

    // Improve focus visibility
    document.body.addEventListener('mousedown', () => {
      document.body.classList.add('using-mouse');
    });

    document.body.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        document.body.classList.remove('using-mouse');
      }
    });
  }


  // ============================================
  // INITIALIZE
  // ============================================

  function init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initAll);
    } else {
      initAll();
    }
  }

  function initAll() {
    initLanguageToggle();
    initMobileNav();
    initNavbarScroll();
    initSmoothScroll();
    initScrollAnimations();
    initCounters();
    setCurrentYear();
    initAccessibility();

  }

  init();
})();
