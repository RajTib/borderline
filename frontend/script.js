// Initialize map
const map = L.map('map').setView([12.9716, 79.1588], 15); // VIT-ish coords

// Add tile layer (actual map visuals)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

map.on('click', function (e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;

    console.log("Clicked:", lat, lon);
});
