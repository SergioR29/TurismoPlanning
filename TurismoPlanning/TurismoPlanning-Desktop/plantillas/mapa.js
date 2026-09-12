var mymap = null; // Variable para el mapa
var initialZoom = 15; // Nivel de zoom inicial cuando se obtiene ubicación

// Función de éxito al obtener la ubicación
function onLocationFound(e) { // 'e' es el objeto Position de la API Geolocation
    // Eliminar el mensaje de estado
    var statusDiv = document.getElementById('status-message');
    if (statusDiv) {
        statusDiv.style.display = 'none';
    }

    // --- ¡CORRECCIÓN AQUÍ! Acceder a las coordenadas desde e.coords ---
    var lat = e.coords.latitude;
    var lon = e.coords.longitude;
    var accuracy = e.coords.accuracy; // La precisión también está en e.coords
    var radius = accuracy / 2;

    var locationLatLng = L.latLng(lat, lon); // Crear un objeto L.LatLng de Leaflet

    // --- Usar el objeto L.LatLng (locationLatLng) o las coordenadas individuales ---

    if (mymap === null) {
         // Si el mapa no está inicializado, crearlo y centrarlo en la ubicación detectada
         mymap = L.map('mapid').setView(locationLatLng, initialZoom); // Usar el objeto L.LatLng

         L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
             maxZoom: 19,
             attribution: '© OpenStreetMap contributors'
         }).addTo(mymap);

         // Opcional: Añadir un círculo que muestre la precisión
         L.circle(locationLatLng, radius).addTo(mymap); // Usar el objeto L.LatLng

         // Añadir un marcador en la ubicación detectada
         L.marker(locationLatLng).addTo(mymap) // Usar el objeto L.LatLng
             .bindPopup("¡Estás aquí! Precisión: " + accuracy + " metros.").openPopup(); // Usar 'accuracy' directamente

    } else {
        // Si el mapa ya está inicializado (ej. si usas watchPosition o inicialización por defecto)
        // Puedes simplemente centrar la vista o actualizar marcador/círculo existentes
        mymap.setView(locationLatLng, initialZoom);
        // Lógica para actualizar marcador y círculo existentes si es necesario (ej. moverlos a locationLatLng)
    }

     console.log("Ubicación encontrada:", locationLatLng, "Precisión:", accuracy); // Imprimir en la consola
}

// Función de error al obtener la ubicación
function onLocationError(e) { // 'e' es el objeto GeolocationPositionError
     var statusDiv = document.getElementById('status-message');
     if (statusDiv) {
         statusDiv.style.backgroundColor = 'pink';
         statusDiv.innerText = 'Error al obtener ubicación: ' + e.message;
         // No ocultar completamente el mensaje, mostrar el error
     }

    console.error("Error de Geolocation:", e.message); // Imprimir en la consola

     // Opcional: Mostrar un mapa por defecto si falla la detección de ubicación
     if (mymap === null) {
         console.log("Mostrando mapa por defecto (Madrid)...");
         // Centrar en Madrid por defecto
         mymap = L.map('mapid').setView([40.416775, -3.703790], 13);
         L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
             maxZoom: 19,
             attribution: '© OpenStreetMap contributors'
         }).addTo(mymap);
     } else {
         // Si el mapa ya existe pero la detección falla, puedes resetear la vista o mostrar un mensaje sobre el mapa
         console.log("Geolocation falló, manteniendo vista actual o por defecto.");
     }
}

// --- Llamar a la API de Geolocation del navegador ---
// Comprobar si el navegador soporta Geolocation
if ('geolocation' in navigator) {
    console.log("Geolocation disponible. Intentando obtener ubicación..."); // Imprimir en la consola
     // Opciones para getCurrentPosition
    var geoOptions = {
         enableHighAccuracy: true, // Intentar usar el mejor método (GPS si es posible)
         timeout: 15000, // Tiempo máximo para obtener la ubicación (15 segundos)
         maximumAge: 0 // No usar ubicaciones en caché, obtener una nueva
    };
    navigator.geolocation.getCurrentPosition(onLocationFound, onLocationError, geoOptions);

    // Si quieres seguir la ubicación mientras el usuario se mueve, usa watchPosition en lugar de getCurrentPosition
    // navigator.geolocation.watchPosition(onLocationFound, onLocationError, geoOptions);

} else {
    // Geolocation no soportado por el navegador (o QWebEngineView)
     var statusDiv = document.getElementById('status-message');
     if (statusDiv) {
         statusDiv.style.backgroundColor = 'pink';
         statusDiv.innerText = 'Error: Geolocation no soportado por este navegador.';
     }
     console.error("Error: Geolocation no soportado."); // Imprimir en la consola

     // Mostrar un mapa por defecto si Geolocation no soportado
     if (mymap === null) {
         console.log("Geolocation no soportado. Mostrando mapa por defecto (Madrid)...");
         mymap = L.map('mapid').setView([40.416775, -3.703790], 13); // Madrid por defecto
         L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
             maxZoom: 19,
             attribution: '© OpenStreetMap contributors'
         }).addTo(mymap);
     }
}
