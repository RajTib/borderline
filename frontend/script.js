// Initialize map
const map = L.map('map').setView([12.9716, 79.1588], 15);

// Add tile layer (actual map visuals)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(map);

map.on('click', async function (e) {
    const lat = e.latlng.lat;
    const lon = e.latlng.lng;

    console.log("Sending:", lat, lon);

    await fetch("http://127.0.0.1:8000/update-location", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: 1,
            lat: lat,
            lon: lon
        })
    });
});
