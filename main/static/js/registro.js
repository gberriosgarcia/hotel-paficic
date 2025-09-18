document.addEventListener('DOMContentLoaded', () => {
  // Año en el footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();


  });

  function setBodyPaddingFromNavbar() {
      const nav = document.querySelector('.navbar');
      if (!nav) return;
      const h = nav.offsetHeight || 72;
      document.documentElement.style.setProperty('--nav-h', h + 'px');
    }
    window.addEventListener('load', setBodyPaddingFromNavbar);
    window.addEventListener('resize', setBodyPaddingFromNavbar);