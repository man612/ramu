(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('motion-ready');

  const pageEnter = document.createElement('div');
  pageEnter.className = 'page-enter';
  pageEnter.setAttribute('aria-hidden', 'true');
  document.body.prepend(pageEnter);
  window.setTimeout(() => pageEnter.remove(), 900);

  const revealSelectors = [
    '.section-kicker', '.intro-grid', '.before-after', '.section-heading', '.use-grid',
    '.foundation-grid', '.pack-header', '.pack-bottom', '.trust-grid', '.faq-list',
    '.closing-inner', '.setup-intro', '.setup-summary-card', '.setup-step-card', '.site-footer'
  ];

  revealSelectors.forEach(selector => {
    document.querySelectorAll(selector).forEach(el => {
      if (!el.hasAttribute('data-reveal')) el.setAttribute('data-reveal', '');
    });
  });

  const staggerSelectors = ['.before-after', '.use-grid', '.foundation-grid', '.course-cards', '.trust-grid', '.prompt-grid'];
  staggerSelectors.forEach(selector => {
    document.querySelectorAll(selector).forEach(container => {
      container.setAttribute('data-stagger', '');
      [...container.children].forEach((child, index) => child.style.setProperty('--stagger-index', index));
    });
  });

  if (!reduceMotion && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });

    document.querySelectorAll('[data-reveal], [data-stagger]').forEach(el => revealObserver.observe(el));
  } else {
    document.querySelectorAll('[data-reveal], [data-stagger]').forEach(el => el.classList.add('is-visible'));
  }

  let previousY = window.scrollY;
  let ticking = false;
  const header = document.querySelector('.site-header');

  function updateScrollUI() {
    const y = window.scrollY;
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    document.documentElement.style.setProperty('--page-progress', Math.min(1, y / max));

    if (header) {
      header.classList.toggle('is-scrolled', y > 18);
      const movingDown = y > previousY;
      const shouldHide = movingDown && y > 180 && Math.abs(y - previousY) > 2;
      header.classList.toggle('is-hidden', shouldHide);
      if (!movingDown) header.classList.remove('is-hidden');
    }
    previousY = y;
    ticking = false;
  }

  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateScrollUI);
  }, { passive: true });
  updateScrollUI();

  document.querySelectorAll('.button, .small-button, .prompt-grid button').forEach(button => {
    button.setAttribute('data-magnetic', '');
    button.addEventListener('pointerdown', event => {
      const rect = button.getBoundingClientRect();
      button.style.setProperty('--ripple-x', `${event.clientX - rect.left}px`);
      button.style.setProperty('--ripple-y', `${event.clientY - rect.top}px`);
      button.classList.remove('is-rippling');
      requestAnimationFrame(() => button.classList.add('is-rippling'));
      setTimeout(() => button.classList.remove('is-rippling'), 680);
    });
  });

  if (!reduceMotion && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('[data-magnetic]').forEach(el => {
      el.addEventListener('pointermove', event => {
        const rect = el.getBoundingClientRect();
        const x = (event.clientX - rect.left - rect.width / 2) * 0.1;
        const y = (event.clientY - rect.top - rect.height / 2) * 0.16;
        el.style.transform = `translate(${x}px, ${y}px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });

    const phoneStage = document.querySelector('.phone-stage');
    const phone = phoneStage?.querySelector('.phone-card:not(.phone-back)');
    if (phoneStage && phone) {
      phoneStage.addEventListener('pointermove', event => {
        const rect = phoneStage.getBoundingClientRect();
        const nx = (event.clientX - rect.left) / rect.width - .5;
        const ny = (event.clientY - rect.top) / rect.height - .5;
        phone.style.setProperty('--phone-ry', `${nx * 9}deg`);
        phone.style.setProperty('--phone-rx', `${ny * -7}deg`);
        phone.style.setProperty('--phone-y', `${ny * -7}px`);
      });
      phoneStage.addEventListener('pointerleave', () => {
        phone.style.setProperty('--phone-ry', '0deg');
        phone.style.setProperty('--phone-rx', '0deg');
        phone.style.setProperty('--phone-y', '0px');
      });
    }
  }

  const marker = document.querySelector('.marker');
  if (marker && 'IntersectionObserver' in window) {
    const markerObserver = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) {
        marker.classList.add('is-animated');
        markerObserver.disconnect();
      }
    }, { threshold: .7 });
    markerObserver.observe(marker);
  }

  function enhanceCourseCards(root = document) {
    root.querySelectorAll?.('.course-card').forEach(card => {
      if (card.dataset.motionEnhanced) return;
      card.dataset.motionEnhanced = 'true';
      card.addEventListener('pointermove', event => {
        if (!matchMedia('(hover: hover) and (pointer: fine)').matches) return;
        const rect = card.getBoundingClientRect();
        card.style.setProperty('--card-x', `${event.clientX - rect.left}px`);
        card.style.setProperty('--card-y', `${event.clientY - rect.top}px`);
      });
    });
  }
  enhanceCourseCards();

  function setupDynamicStagger(root = document) {
    root.querySelectorAll?.('.course-cards, .prompt-grid').forEach(container => {
      container.setAttribute('data-stagger', '');
      [...container.children].forEach((child, index) => child.style.setProperty('--stagger-index', index));
      requestAnimationFrame(() => container.classList.add('is-visible'));
    });
  }

  const dynamicObserver = new MutationObserver(mutations => {
    mutations.forEach(mutation => mutation.addedNodes.forEach(node => {
      if (!(node instanceof Element)) return;
      enhanceCourseCards(node.parentElement || node);
      setupDynamicStagger(node.parentElement || node);
      node.querySelectorAll?.('.button, .small-button, .prompt-grid button').forEach(button => {
        if (button.dataset.motionButton) return;
        button.dataset.motionButton = 'true';
        button.addEventListener('pointerdown', event => {
          const rect = button.getBoundingClientRect();
          button.style.setProperty('--ripple-x', `${event.clientX - rect.left}px`);
          button.style.setProperty('--ripple-y', `${event.clientY - rect.top}px`);
          button.classList.remove('is-rippling');
          requestAnimationFrame(() => button.classList.add('is-rippling'));
          setTimeout(() => button.classList.remove('is-rippling'), 680);
        });
      });
    }));
  });
  dynamicObserver.observe(document.body, { childList: true, subtree: true });

  const setupSections = [...document.querySelectorAll('.setup-step-card[id]')];
  const setupLinks = [...document.querySelectorAll('.setup-nav a[href^="#"]')];
  if (setupSections.length && 'IntersectionObserver' in window) {
    const stepObserver = new IntersectionObserver(entries => {
      const visible = entries
        .filter(entry => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      setupSections.forEach(section => section.classList.toggle('is-current-step', section === visible.target));
      setupLinks.forEach(link => link.classList.toggle('is-current', link.getAttribute('href') === `#${visible.target.id}`));
    }, { threshold: [0.25, 0.45, 0.7], rootMargin: '-18% 0px -48% 0px' });
    setupSections.forEach(section => stepObserver.observe(section));
  }

  function burstFrom(element) {
    if (reduceMotion || !element) return;
    const rect = element.getBoundingClientRect();
    const palette = ['#b96a43', '#9b7a36', '#496354', '#55759b', '#765f77'];
    for (let i = 0; i < 12; i += 1) {
      const particle = document.createElement('i');
      particle.className = 'motion-particle';
      particle.style.left = `${rect.left + rect.width / 2}px`;
      particle.style.top = `${rect.top + rect.height / 2}px`;
      const angle = (Math.PI * 2 * i) / 12 + Math.random() * .25;
      const distance = 38 + Math.random() * 52;
      particle.style.setProperty('--particle-x', `${Math.cos(angle) * distance}px`);
      particle.style.setProperty('--particle-y', `${Math.sin(angle) * distance}px`);
      particle.style.setProperty('--particle-r', `${Math.random() * 280 - 140}deg`);
      particle.style.setProperty('--particle-color', palette[i % palette.length]);
      document.body.appendChild(particle);
      setTimeout(() => particle.remove(), 820);
    }
  }

  document.addEventListener('change', event => {
    const input = event.target;
    if (!(input instanceof HTMLInputElement) || input.type !== 'checkbox' || !input.checked) return;
    burstFrom(input.closest('label') || input);
  });

  document.addEventListener('click', event => {
    const copyButton = event.target.closest('#copy-instructions, .copy-project, .copy-course-pack, [data-copy-phrase]');
    if (copyButton) burstFrom(copyButton);
  });

  const faqItems = document.querySelectorAll('.faq-list details');
  faqItems.forEach(item => {
    item.addEventListener('toggle', () => {
      if (!item.open) return;
      faqItems.forEach(other => {
        if (other !== item && other.open) other.open = false;
      });
    });
  });

  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      event.preventDefault();
      const headerOffset = 92;
      const top = target.getBoundingClientRect().top + scrollY - headerOffset;
      window.scrollTo({ top, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });
})();
