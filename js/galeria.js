document.addEventListener('DOMContentLoaded', () => {
  // Año en footer
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Cargar imagen en el modal desde el thumbnail clickeado
  const modal = document.getElementById('viewerModal');
  if (modal) {
    modal.addEventListener('show.bs.modal', (ev) => {
      const trigger = ev.relatedTarget; // <a> que abrió el modal
      const src = trigger?.getAttribute('data-viewer-src');
      const alt = trigger?.querySelector('img')?.getAttribute('alt') || 'Foto habitación';
      const img = modal.querySelector('#viewerImg');
      if (img && src) {
        img.src = src;
        img.alt = alt;
      }
    });
  }
});