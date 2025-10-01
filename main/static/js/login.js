// main/static/js/login.js
// Toggle mostrar/ocultar contraseña + footer year (robusto)
(function () {
  function $(id) { return document.getElementById(id); }

  function init() {
    // Año en el footer
    const yearEl = $('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // Soportar varios ids habituales para el input de contraseña
    const possiblePassIds = ['password', 'loginPass', 'login-pass', 'pass'];
    let passInput = null;
    for (const id of possiblePassIds) {
      passInput = $(id);
      if (passInput) break;
    }

    // Soportar varios ids para el botón toggle
    const possibleBtnIds = ['togglePass', 'toggle-pass', 'togglePassword'];
    let toggleBtn = null;
    for (const id of possibleBtnIds) {
      toggleBtn = $(id);
      if (toggleBtn) break;
    }

    // Si no encontró elementos, no rompe
    if (!toggleBtn || !passInput) {
      // console.log('login.js: toggleBtn or passInput not found', { toggleBtn, passInput });
      return;
    }

    // Evitar añadir múltiples listeners si ya existe
    if (toggleBtn._hasToggleHandler) return;

    const handler = function (e) {
      e.preventDefault();
      if (passInput.type === 'password') {
        passInput.type = 'text';
        toggleBtn.textContent = 'Ocultar';
        toggleBtn.setAttribute('aria-pressed', 'true');
      } else {
        passInput.type = 'password';
        toggleBtn.textContent = 'Mostrar';
        toggleBtn.setAttribute('aria-pressed', 'false');
      }
      try { passInput.focus(); } catch (err) { /* ignore */ }
    };

    toggleBtn.addEventListener('click', handler);
    toggleBtn._hasToggleHandler = true;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
