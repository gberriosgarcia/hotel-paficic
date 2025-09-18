// Traducción automática español/inglés para home.html
const traducciones = {
	es: {
		'Inicio': 'Inicio',
		'Registro': 'Registro',
		'Habitaciones': 'Habitaciones',
		'Galeria': 'Galería',
		'Contacto': 'Contacto',
		'Bienvenido a Hotel Pacific Reef': 'Bienvenido a Hotel Pacific Reef',
		'Nuestro hotel cuenta con <strong>38 habitaciones</strong> distribuidas en siete pisos: <strong>5 pisos de categoría Turista</strong> con <strong>6 habitaciones por piso</strong> (30 en total), y <strong>2 pisos Premium</strong> con <strong>4 habitaciones por piso</strong> (8 en total).': 'Nuestro hotel cuenta con <strong>38 habitaciones</strong> distribuidas en siete pisos: <strong>5 pisos de categoría Turista</strong> con <strong>6 habitaciones por piso</strong> (30 en total), y <strong>2 pisos Premium</strong> con <strong>4 habitaciones por piso</strong> (8 en total).',
		'Registrar huésped': 'Registrar huésped',
		'Ver habitaciones': 'Ver habitaciones',
		'Resumen de capacidad': 'Resumen de capacidad',
		'Habitaciones': 'Habitaciones',
		'Turista (5×6)': 'Turista (5×6)',
		'Premium (2×4)': 'Premium (2×4)',
		'*Capacidad total informada por el propietario.': '*Capacidad total informada por el propietario.',
		'Categorías de habitaciones': 'Categorías de habitaciones',
		'Distribución por tipo y piso': 'Distribución por tipo y piso',
		'Turista': 'Turista',
		'Habitaciones cómodas y funcionales en los primeros 5 pisos.': 'Habitaciones cómodas y funcionales en los primeros 5 pisos.',
		'Pisos': 'Pisos',
		'Por piso': 'Por piso',
		'Total': 'Total',
		'Ver detalle': 'Ver detalle',
		'Premium': 'Premium',
		'Habitaciones superiores con mejor vista en los 2 pisos superiores.': 'Habitaciones superiores con mejor vista en los 2 pisos superiores.',
		'Ir a registro': 'Ir a registro',
		'© <span id="year"></span> Hotel Pacific Reef · Todos los derechos reservados': '© <span id="year"></span> Hotel Pacific Reef · Todos los derechos reservados'
	},
	en: {
		'Inicio': 'Home',
		'Registro': 'Register',
		'Habitaciones': 'Rooms',
		'Galeria': 'Gallery',
		'Contacto': 'Contact',
		'Bienvenido a Hotel Pacific Reef': 'Welcome to Pacific Reef Hotel',
		'Nuestro hotel cuenta con <strong>38 habitaciones</strong> distribuidas en siete pisos: <strong>5 pisos de categoría Turista</strong> con <strong>6 habitaciones por piso</strong> (30 en total), y <strong>2 pisos Premium</strong> con <strong>4 habitaciones por piso</strong> (8 en total).': 'Our hotel has <strong>38 rooms</strong> distributed over seven floors: <strong>5 Tourist category floors</strong> with <strong>6 rooms per floor</strong> (30 total), and <strong>2 Premium floors</strong> with <strong>4 rooms per floor</strong> (8 total).',
		'Registrar huésped': 'Register guest',
		'Ver habitaciones': 'View rooms',
		'Resumen de capacidad': 'Capacity summary',
		'Habitaciones': 'Rooms',
		'Turista (5×6)': 'Tourist (5×6)',
		'Premium (2×4)': 'Premium (2×4)',
		'*Capacidad total informada por el propietario.': '*Total capacity reported by owner.',
		'Categorías de habitaciones': 'Room categories',
		'Distribución por tipo y piso': 'Distribution by type and floor',
		'Turista': 'Tourist',
		'Habitaciones cómodas y funcionales en los primeros 5 pisos.': 'Comfortable and functional rooms on the first 5 floors.',
		'Pisos': 'Floors',
		'Por piso': 'Per floor',
		'Total': 'Total',
		'Ver detalle': 'View details',
		'Premium': 'Premium',
		'Habitaciones superiores con mejor vista en los 2 pisos superiores.': 'Superior rooms with better views on the top 2 floors.',
		'Ir a registro': 'Go to register',
		'© <span id="year"></span> Hotel Pacific Reef · Todos los derechos reservados': '© <span id="year"></span> Pacific Reef Hotel · All rights reserved'
	}
};

function setLanguage(lang) {
	localStorage.setItem('idioma', lang);
	translatePage(lang);
}

function translatePage(lang) {
	const dict = traducciones[lang];
	if (!dict) return;
	// Traducción de textos exactos
	Object.keys(dict).forEach(key => {
		document.querySelectorAll('*').forEach(el => {
			if (el.childNodes.length === 1 && el.childNodes[0].nodeType === 3 && el.textContent.trim() === key) {
				el.textContent = dict[key];
			}
			// Traducción de innerHTML exacto (para textos con etiquetas)
			if (el.innerHTML.trim() === key) {
				el.innerHTML = dict[key];
			}
		});
	});
}

document.addEventListener('DOMContentLoaded', () => {
	const lang = localStorage.getItem('idioma') || 'es';
	translatePage(lang);
});
// Copia aquí el contenido de js/idioma.js
