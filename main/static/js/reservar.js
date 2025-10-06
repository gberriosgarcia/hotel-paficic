// static/js/reserva.js
document.addEventListener('DOMContentLoaded', function () {
  // Año footer
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Campos de salida (solo lectura)
  const tipoOut = document.getElementById('tipoDisplay');
  const precioOut = document.getElementById('precioDisplay');
  const adelantoOut = document.getElementById('adelantoDisplay');

  // Selects posibles
  const selHabitacion = document.getElementById('habitacion_id'); // flujo por habitación
  const selTipo = document.getElementById('tipo');                // flujo por tipo (turista/premium)

  // Datos inyectados por Django para el flujo por habitación
  const tipoPorHab = window.tipoPorHab || null;

  // Precios fijos de negocio
  const PRICE = { TURISTA: 90.00, PREMIUM: 180.00 };
  const RATE = 0.30;

  function setOutputs(t, base) {
    if (tipoOut)   tipoOut.value   = t || '—';
    if (precioOut) precioOut.value = (base != null) ? base.toFixed(2) : '—';
    if (adelantoOut) {
      if (base != null) {
        adelantoOut.value = (base * RATE).toFixed(2);
      } else {
        adelantoOut.value = '—';
      }
    }
  }

  function normalizeTipoFromForm(v) {
    const s = String(v || '').toLowerCase();
    if (['premium', 'premier', 'vip', 'suite'].includes(s)) return 'PREMIUM';
    // single/double/doble/turista/normal/otros => TURISTA
    return 'TURISTA';
  }

  // --- Modo A: seleccionar habitación con mapa servidor ---
  function updateFromHabitacion() {
    const id = selHabitacion && selHabitacion.value;
    if (!id || !tipoPorHab || !tipoPorHab[id]) {
      setOutputs(null, null);
      return;
    }
    const info = tipoPorHab[id]; // { tipo, base, adelanto } (base/adelanto son strings)
    const tipo = info.tipo || 'TURISTA';
    const base = info.base ? parseFloat(info.base) : (PRICE[tipo] || PRICE.TURISTA);
    setOutputs(tipo, base);
  }

  // --- Modo B: seleccionar tipo directamente ---
  function updateFromTipo() {
    const t = normalizeTipoFromForm(selTipo && selTipo.value);
    const base = PRICE[t] || PRICE.TURISTA;
    setOutputs(t, base);
  }

  // Enganche de eventos según lo que exista en el DOM
  if (selHabitacion && tipoPorHab) {
    selHabitacion.addEventListener('change', updateFromHabitacion);
    updateFromHabitacion();
  } else if (selTipo) {
    selTipo.addEventListener('change', updateFromTipo);
    updateFromTipo();
  } else {
    // No hay select reconocido; limpia salidas
    setOutputs(null, null);
  }
});
