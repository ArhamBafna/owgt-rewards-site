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

  // Live item count updater from data.json
  function updateLiveCounts() {
    fetch('/data.json')
      .then(function (res) {
        if (!res.ok) throw new Error('Failed to fetch data.json');
        return res.json();
      })
      .then(function (data) {
        if (!data || !Array.isArray(data.items)) return;
        var total = data.items.length;

        // 1. Hero number
        var heroNum = document.querySelector('.landing-hero-num[data-hero-count]') || document.querySelector('.landing-hero-num:first-of-type');
        if (heroNum) {
          heroNum.textContent = total;
        }

        // 2. Marquee text
        document.querySelectorAll('.marquee__text').forEach(function (el) {
          if (/\d+\s+resources/i.test(el.textContent)) {
            el.textContent = el.textContent.replace(/\d+\s+resources/i, total + ' resources');
          }
        });

        // 3. Hero proof text
        var proof = document.querySelector('.landing-hero__proof');
        if (proof && /\d+\s+resources/i.test(proof.textContent)) {
          proof.textContent = proof.textContent.replace(/\d+\s+resources/i, total + ' resources');
        }

        // 4. Section intros
        document.querySelectorAll('.section-intro').forEach(function (intro) {
          if (/\d+\s+items\s+across/i.test(intro.textContent)) {
            intro.textContent = intro.textContent.replace(/\d+\s+items\s+across/i, total + ' items across');
          }
          if (/\d+\s+AI\s+resources/i.test(intro.textContent)) {
            intro.textContent = intro.textContent.replace(/\d+\s+AI\s+resources/i, total + ' AI resources');
          }
        });

        // 5. Category breakdown
        var catCounts = {};
        data.items.forEach(function (it) {
          var c = (it.category || it.folder_category || '').trim().toLowerCase();
          if (c) catCounts[c] = (catCounts[c] || 0) + 1;
        });

        document.querySelectorAll('.category-browse .card, .card-grid .card').forEach(function (card) {
          var titleEl = card.querySelector('.card__title');
          var metaEl = card.querySelector('.card__footer .meta');
          if (titleEl && metaEl) {
            var catName = titleEl.textContent.trim().toLowerCase();
            if (catCounts[catName] !== undefined) {
              metaEl.textContent = catCounts[catName] + ' items';
            }
          }
        });
      })
      .catch(function (err) {
        console.warn('Live count update skipped:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateLiveCounts);
  } else {
    updateLiveCounts();
  }
})();
