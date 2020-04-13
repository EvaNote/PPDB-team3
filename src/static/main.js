// make a map that will be placed on the 'Find my ride' page
let map = L.map('findride_map').setView([51, 4.4], 10);

$(document).ready(function () {
    //TODO: dropdown? Lijst? Niks?
    document.getElementsByClassName('leaflet-routing-geocoder')[1].remove();
    document.getElementsByClassName('leaflet-routing-add-waypoint')[0].remove();
    let el = document.createTextNode('Kies een campus op de kaart (geen campus gekozen)');
    document.getElementsByClassName('leaflet-routing-geocoders')[0].appendChild(el)

    //src: https://github.com/pointhi/leaflet-color-markers
    var universityIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    var collegeIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    $.post({
        contentType: "application/json",
        url: "/en/fillschools"
    })
    // when post request is done, get the returned data and do something with it
        .done(function (markers) { // response function
            for (var i in markers) {
                let hover_display = markers[i].display_name;
                hover_display = hover_display.substr(0, hover_display.length - 29);
                let icon = null;
                if (markers[i].soort === 'u') {
                    icon = universityIcon
                } else {
                    icon = collegeIcon
                }

                (L.marker([markers[i].lat, markers[i].lon], {icon: icon, name: hover_display})
                    .bindPopup('<a href="' + markers[i].url + '" target="_blank">' + markers[i].name + '</a>')
                    .addTo(map))
                    .on({
                        'mouseover': function (e) {
                            var container = L.DomUtil.create('div');
                            container.appendChild(document.createTextNode(this.options['name']));
                            L.popup({
                                offset: [0, -30]
                            })
                                .setContent(container)
                                .setLatLng(e.latlng)
                                .openOn(map);
                        },
                        'mouseout': function (e) {
                            setTimeout(function () {
                                map.closePopup();
                            }, 2500)
                        }
                    })
            }
        });
});



// add a tile layer to the (empty) map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function createButton(label, container) {
    var btn = L.DomUtil.create('button', '', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}

map.on('click', function (e) {
    var container = L.DomUtil.create('div'),
        startBtn = createButton('Start from this location', container),
        destBtn = createButton('Go to this location', container);

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(map);
    L.DomEvent.on(startBtn, 'click', function () {
        control.spliceWaypoints(0, 1, e.latlng);
        map.closePopup();
    });

    L.DomEvent.on(destBtn, 'click', function () {
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
        map.closePopup();
    });
});
// add OSRM support using Leaflet Routing Machine
let control = L.Routing.control({
    serviceUrl: 'http://127.0.0.1:5001/route/v1',
    routeWhileDragging: true,
    geocoder: L.Control.Geocoder.nominatim()
})
// when route is found, send coordinates of start and end to /en/receiver
    .on('routesfound', function (e) {
        let from = e.waypoints[0].latLng;
        let to = e.waypoints[1].latLng;
        $.post({
            contentType: "application/json",
            url: "/en/receiver",
            data: JSON.stringify({from: from, to: to})
        })
        // when post request is done, get the returned data and do something with it
            .done(function (data) { // response function
                alert("Result: " + data);
            });
    }).addTo(map);
