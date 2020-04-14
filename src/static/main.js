/** loop and retrieve all waypoints:
 const values = Object.values(e.waypoints)
 for (const value of values) {
            console.log(value.latLng.lat)
        }
 */


// make a map that will be placed on the 'Find my ride' page
let map = L.map('findride_map').setView([51, 4.4], 10);

// add a tile layer to the (empty) map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// add OSRM support using Leaflet Routing Machine
let control = L.Routing.control({
    serviceUrl: 'http://127.0.0.1:5001/route/v1',
    routeWhileDragging: true,
    geocoder: L.Control.Geocoder.nominatim(),
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

/**************
 * jQuery functions
 * ************/

$(document).ready(function () {
    //TODO: dropdown? Lijst? Niks?
    document.getElementsByClassName('leaflet-routing-geocoder')[1].remove();
    document.getElementsByClassName('leaflet-routing-add-waypoint')[0].remove();
    let child = document.createElement('div');
    child.innerHTML = "<p>Kies een campus op de kaart (geen campus gekozen)</p>";
    child = child.firstChild;
    document.getElementsByClassName('leaflet-routing-geocoders')[0].appendChild(child);
    // add time form
    child = document.createElement('div');
    child.innerHTML = "<form action=\"#\" id=\"ride-time\">\n" +
        "    <label for=\"time_option\">\n<select name=\"time_option\">\n" +
        "        <option>Arrive by</option>\n" +
        "        <option>Depart at</option>\n" +
        "    </select>\n" +
        "        <input id=\"time_input\" type=\"datetime-local\" name=\"datetime\">\n" +
        "    </label>\n" +
        "    <input type=\"submit\" value=\"Update\">\n" +
        "</form>";
    child = child.firstChild;
    document.getElementsByClassName('leaflet-routing-geocoders')[0].appendChild(child);

    //src: https://github.com/pointhi/leaflet-color-markers
    var universityIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [20, 32],
        iconAnchor: [7, 32],
        popupAnchor: [1, -20],
        shadowSize: [32, 32]
    });

    var collegeIcon = new L.Icon({
        iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-violet.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [20, 32],
        iconAnchor: [7, 32],
        popupAnchor: [1, -20],
        shadowSize: [32, 32]
    });

    $.post({
        contentType: "application/json",
        url: "/en/fillschools"
    })
        // when post request is done, get the returned data and do something with it
        .done(function (markers) { // response function
            for (var i in markers) {
                let hover_display = markers[i].name;
                //hover_display = hover_display.substr(0, hover_display.length - 29);
                let icon = null;
                if (markers[i].category === 'university') {
                    icon = universityIcon
                } else {
                    icon = collegeIcon
                }

                (L.marker([markers[i].latitude, markers[i].longitude], {
                    icon: icon,
                    name: hover_display,
                    id: markers[i].id
                })
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
                        },
                        'click': function (e) {
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
                        }
                    })
            }
        });
});

$.fn.setNow = function (onlyBlank) {
    /**
     * get current date and time and format it
     * source: https://stackoverflow.com/questions/24468518/html5-input-datetime-local-default-value-of-today-and-current-time
     */
    let now = new Date($.now()), year, month, date, hours, minutes, formattedDateTime;
    year = now.getFullYear();
    month = now.getMonth().toString().length === 1 ? '0' + (now.getMonth() + 1).toString() : now.getMonth() + 1;
    date = now.getDate().toString().length === 1 ? '0' + (now.getDate()).toString() : now.getDate();
    hours = now.getHours().toString().length === 1 ? '0' + now.getHours().toString() : now.getHours();
    minutes = now.getMinutes().toString().length === 1 ? '0' + now.getMinutes().toString() : now.getMinutes();
    formattedDateTime = year + '-' + month + '-' + date + 'T' + hours + ':' + minutes;
    if (onlyBlank === true && $(this).val()) {
        return this;
    }
    $(this).val(formattedDateTime);
    return this;
}

$.fn.serializeObject = function () {
    /**
     * make sure that pressing the 'update' button doesn't refresh the entire page
     */
    let o = {};
    let a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$(function () {
    // make sure pressing the 'update' button doesn't refresh the entire page
    $('form').submit(function () {
        let from = control.getWaypoints()[0].latLng;
        let to = control.getWaypoints()[1].latLng;
        let form = $('form').serializeObject();
        // check if from-to are defined. If they aren't, nothing should happen
        if (typeof from !== 'undefined' && typeof to !== 'undefined') {
            $.post({
                contentType: "application/json",
                url: "/en/calculateCompatibleRides",
                data: JSON.stringify({from: from, to: to, time_option: form.time_option, datetime: form.datetime})
            })
                // when post request is done, get the returned data and do something with it
                .done(function (data) { // response function
                    alert("Result: " + data);
                });
        }
        return false;
    });

    // insert the current date and time in the correct input field
    $('input[type="datetime-local"]').setNow();
});