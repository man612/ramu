(() => {
  if (!window.matchMedia('(max-width: 720px)').matches) return;

  const dock = document.createElement('nav');
  dock.className = 'mobile-dock';
  dock.setAttribute('aria-label', 'Navigasi cepat mobile');

  const isSetup = Boolean(document.querySelector('.setup-main'));

  if (isSetup) {
    dock.innerHTML = `
      <a href="./"><span class="dock-icon">⌂</span><span>Beranda</span></a>
      <button type="button" class="dock-progress" id="dock-progress"><strong>0/5</strong><span>Project</span></button>
      <a href="https://chatgpt.com/" target="_blank" rel="noopener" class="dock-primary"><span class="dock-icon">↗</span><span>Buka ChatGPT</span></a>
    `;
  } else {
    dock.innerHTML = `
      <a href="#cara-pakai"><span class="dock-icon">↓</span><span>Cara pakai</span></a>
      <a href="setup.html" class="dock-primary"><span class="dock-icon">＋</span><span>Mulai setup</span></a>
      <a href="#paket"><span class="dock-icon">▦</span><span>Paket</span></a>
    `;
  }

  document.body.appendChild(dock);

  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  dock.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      const target = document.querySelector(link.getAttribute('href'));
      if (!target) return;
      event.preventDefault();
      const top = target.getBoundingClientRect().top + scrollY - 76;
      window.scrollTo({ top, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  });

  if (isSetup) {
    const dockProgress = dock.querySelector('#dock-progress strong');
    const source = document.querySelector('#progress-title');

    const syncProgress = () => {
      if (!dockProgress || !source) return;
      const match = source.textContent.match(/(\d+)\s+dari\s+(\d+)/i);
      dockProgress.textContent = match ? `${match[1]}/${match[2]}` : '0/5';
    };

    syncProgress();
    if (source) new MutationObserver(syncProgress).observe(source, { childList: true, characterData: true, subtree: true });

    dock.querySelector('#dock-progress')?.addEventListener('click', () => {
      const target = document.querySelector('#langkah-3');
      if (!target) return;
      window.scrollTo({ top: target.getBoundingClientRect().top + scrollY - 76, behavior: reduceMotion ? 'auto' : 'smooth' });
    });
  }

  let lastY = scrollY;
  let timer;
  addEventListener('scroll', () => {
    const y = scrollY;
    const movingDown = y > lastY;
    if (movingDown && y > 240) dock.classList.add('is-quiet');
    else dock.classList.remove('is-quiet');
    clearTimeout(timer);
    timer = setTimeout(() => dock.classList.remove('is-quiet'), 260);
    lastY = y;
  }, { passive: true });
})();
