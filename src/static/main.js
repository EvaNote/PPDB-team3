let map = L.map('findride_map').setView([51, 4.4], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

map.on('click', function onMapClick(e) {
    let popup = L.popup();
    popup.setLatLng(e.latlng).setContent("You clicked the map at " + e.latlng.toString()).openOn(map);
});

// map.locate({setView: true, maxZoom: 16});
//
// map.on('locationfound', function onLocationFound(e) {
//     let radius = e.accuracy;
//     L.marker(e.latlng).addTo(map).bindPopup("You are within " + radius + " meters from this point").openPopup();
//     L.circle(e.latlng, radius).addTo(map);
// });
//
// map.on('locationerror', function onLocationError(e) {
//     alert(e.message);
// });


L.Routing.control({
    serviceUrl: 'http://127.0.0.1:5001/route/v1',
    waypoints: [
        L.latLng(51.125533, 4.389110),
        L.latLng(51.086153, 4.336953)
    ],
    routeWhileDragging: true
}).addTo(map);

