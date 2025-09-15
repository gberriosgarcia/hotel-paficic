document.addEventListener('DOMContentLoaded', () => {
  // Año en el footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mostrar / ocultar contraseña
  const toggleBtn = document.getElementById('togglePass');
  const passInput = document.getElementById('loginPass');

  if (toggleBtn && passInput) {
    toggleBtn.addEventListener('click', () => {
      const showing = passInput.type === 'text';
      passInput.type = showing ? 'password' : 'text';
      toggleBtn.textContent = showing ? 'Mostrar' : 'Ocultar';
      passInput.focus();
    });
  }
});