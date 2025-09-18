document.addEventListener('DOMContentLoaded', () => {
  // Año en el footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mostrar / ocultar contraseña
  const toggleBtn = document.getElementById('togglePass');
  const passInput = document.getElementById('loginPass');

  if (toggleBtn && passInput) {
    toggleBtn.addEventListener('click', function () {
      if (passInput.type === 'password') {
        passInput.type = 'text';
        toggleBtn.textContent = 'Ocultar';
      } else {
        passInput.type = 'password';
        toggleBtn.textContent = 'Mostrar';
      }
      passInput.focus();
    });
  }
});