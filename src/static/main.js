let map = L.map('findride_map').setView([51, 4.4], 10);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function createButton(label, container) {
    var btn = L.DomUtil.create('button', '', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}
map.on('click', function(e){
        var container = L.DomUtil.create('div'),
        startBtn = createButton('Start from this location', container),
        destBtn = createButton('Go to this location', container);

        L.popup()
            .setContent(container)
            .setLatLng(e.latlng)
            .openOn(map);
        L.DomEvent.on(startBtn, 'click', function() {
            control.spliceWaypoints(0, 1, e.latlng);
            map.closePopup();
        });

        L.DomEvent.on(destBtn, 'click', function() {
            control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
            map.closePopup();
        });
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


let control = L.Routing.control({
    serviceUrl: 'http://127.0.0.1:5001/route/v1',
    waypoints: [
        L.latLng(51.125533, 4.389110),
        L.latLng(51.086153, 4.336953)
    ],
    routeWhileDragging: true,
    geocoder: L.Control.Geocoder.nominatim()
}).addTo(map);

