(() => {
  const header = document.querySelector('.site-header');
  let ticking = false;

  const updateHeader = () => {
    header?.classList.toggle('is-scrolled', window.scrollY > 18);
    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateHeader);
  }, { passive: true });
  updateHeader();

  const setupSections = [...document.querySelectorAll('.setup-step-card[id]')];
  const setupLinks = [...document.querySelectorAll('.setup-nav a[href^="#"]')];

  const setCurrentStep = section => {
    setupSections.forEach(item => item.classList.toggle('is-current-step', item === section));
    setupLinks.forEach(link => {
      const current = link.getAttribute('href') === `#${section.id}`;
      link.classList.toggle('is-current', current);
      if (current) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    });
  };

  if (setupSections.length) {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        const visible = entries
          .filter(entry => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) setCurrentStep(visible.target);
      }, { threshold: [0.25, 0.45, 0.7], rootMargin: '-18% 0px -48% 0px' });
      setupSections.forEach(section => observer.observe(section));
    } else {
      setCurrentStep(setupSections[0]);
    }
  }

  const faqItems = [...document.querySelectorAll('.faq-list details')];
  faqItems.forEach(item => {
    item.addEventListener('toggle', () => {
      if (!item.open) return;
      faqItems.forEach(other => {
        if (other !== item) other.open = false;
      });
    });
  });
})();
