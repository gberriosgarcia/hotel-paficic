(() => {
  'use strict';

  // --- Datos del hotel ---
  const floors = [
    { floor: 1, category: "Turista", rooms: 6 },
    { floor: 2, category: "Turista", rooms: 6 },
    { floor: 3, category: "Turista", rooms: 6 },
    { floor: 4, category: "Turista", rooms: 6 },
    { floor: 5, category: "Turista", rooms: 6 },
    { floor: 6, category: "Premium", rooms: 4 },
    { floor: 7, category: "Premium", rooms: 4 },
  ];

  // Estados de ejemplo (cámbialos por datos reales del backend)
  const preset = {
    Ocupada: [101, 203, 304, 401, 503, 601, 703],
    Limpieza: [105, 205, 402, 602],
    Mantención: [306],
  };

  // Construye el universo de habitaciones con estado
  const allRooms = floors.flatMap(f =>
    Array.from({ length: f.rooms }).map((_, i) => {
      const num = f.floor * 100 + (i + 1);
      let status = "Disponible";
      if (preset.Ocupada.includes(num)) status = "Ocupada";
      else if (preset.Limpieza.includes(num)) status = "Limpieza";
      else if (preset.Mantención?.includes(num)) status = "Mantención";
      return { room: num, floor: f.floor, category: f.category, status };
    })
  );

  // --- Helpers UI ---
  const el = (id) => document.getElementById(id);

  function statusBadge(status) {
    const map = {
      "Disponible": "success",
      "Ocupada": "danger",
      "Limpieza": "warning text-dark",
      "Mantención": "secondary",
    };
    return `<span class="badge bg-${map[status]}">${status}</span>`;
  }

  function statusBorder(status) {
    const map = {
      "Disponible": "border-success",
      "Ocupada": "border-danger",
      "Limpieza": "border-warning",
      "Mantención": "border-secondary",
    };
    return map[status] || "border-secondary";
  }

  // --- Render principal ---
  function render() {
    const fCategory = el('fCategory').value;
    const fFloor = el('fFloor').value;
    const fStatus = el('fStatus').value;
    const fSearch = el('fSearch').value.trim();

    const byFloor = {};
    allRooms.forEach(r => {
      if (fCategory && r.category !== fCategory) return;
      if (fFloor && String(r.floor) !== fFloor) return;
      if (fStatus && r.status !== fStatus) return;
      if (fSearch && !String(r.room).includes(fSearch)) return;
      (byFloor[r.floor] ||= []).push(r);
    });

    const floorKeys = Object.keys(byFloor).sort((a, b) => a - b);
    let html = "";

    floorKeys.forEach(k => {
      const floorNum = Number(k);
      const category = floors.find(f => f.floor === floorNum)?.category || "";
      const rooms = byFloor[k].sort((a, b) => a.room - b.room);

      html += `
        <section class="mb-4">
          <div class="d-flex align-items-center mb-2">
            <h2 class="h5 mb-0">Piso ${floorNum}</h2>
            <span class="ms-2 badge ${category === 'Premium' ? 'bg-warning text-dark' : 'bg-primary'}">${category}</span>
            <span class="ms-auto text-secondary small">${rooms.length} habitaciones visibles</span>
          </div>
          <div class="row row-cols-2 row-cols-sm-3 row-cols-md-4 row-cols-lg-6 g-3">
            ${rooms.map(r => `
              <div class="col">
                <div class="room-tile card text-center ${statusBorder(r.status)} border-2">
                  <div class="card-body py-3">
                    <div class="h5 mb-1">${r.room}</div>
                    ${statusBadge(r.status)}
                  </div>
                  <div class="card-footer small text-secondary bg-transparent">
                    ${r.category}
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </section>
      `;
    });

    if (!floorKeys.length) {
      html = `
        <div class="alert alert-light border d-flex align-items-center" role="alert">
          <div>Sin resultados para los filtros aplicados.</div>
        </div>
      `;
    }

    el('floorsContainer').innerHTML = html;

    // Resumen (sobre el dataset filtrado globalmente)
    const filtered = allRooms.filter(r => {
      if (fCategory && r.category !== fCategory) return false;
      if (fFloor && String(r.floor) !== fFloor) return false;
      if (fStatus && r.status !== fStatus) return false;
      if (fSearch && !String(r.room).includes(fSearch)) return false;
      return true;
    });

    el('countTotal').textContent = filtered.length;
    el('countDisp').textContent = filtered.filter(r => r.status === "Disponible").length;
    el('countOcup').textContent = filtered.filter(r => r.status === "Ocupada").length;
    el('countServ').textContent = filtered.filter(r => r.status === "Limpieza" || r.status === "Mantención").length;
  }

  function init() {
    const form = el('filtersForm');
    if (form) form.addEventListener('input', render);
    const yearEl = el('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
    render();
  }

  document.addEventListener('DOMContentLoaded', init);

  // Exponer para depurar si quieres:
  window.HabitacionesApp = { render };
})();