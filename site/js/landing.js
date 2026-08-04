(function () {
  'use strict';

  var signupSection = document.getElementById('signup');
  var stickyCta = document.getElementById('stickyCta');
  var faqItems = document.querySelectorAll('.landing-faq__item');

  function scrollToSignup() {
    if (signupSection) {
      signupSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  document.querySelectorAll('[data-scroll-signup]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      scrollToSignup();
    });
  });

  if (stickyCta && signupSection) {
    var hero = document.querySelector('.landing-hero');
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            stickyCta.classList.remove('is-visible');
          } else {
            stickyCta.classList.add('is-visible');
          }
        });
      },
      { threshold: 0, rootMargin: '0px 0px -80px 0px' }
    );

    if (hero) {
      observer.observe(hero);
    }

    var signupObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            stickyCta.classList.remove('is-visible');
          }
        });
      },
      { threshold: 0.3 }
    );
    signupObserver.observe(signupSection);
  }

  faqItems.forEach(function (item) {
    var btn = item.querySelector('.landing-faq__question');
    if (!btn) return;

    btn.addEventListener('click', function () {
      var isOpen = item.classList.contains('is-open');

      faqItems.forEach(function (other) {
        other.classList.remove('is-open');
        var otherBtn = other.querySelector('.landing-faq__question');
        if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
      });

      if (!isOpen) {
        item.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });

  var signupForm = document.querySelector('.signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', function (e) {
      e.preventDefault();
    });
  }
})();
