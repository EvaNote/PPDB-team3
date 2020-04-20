/** loop and retrieve all waypoints:
 const values = Object.values(e.waypoints)
 for (const value of values) {
            console.log(value.latLng.lat)
        }



 // get time between waypoints
 let instr = control._line._route.instructions;
 let time = 0;
 for (let i in instr) {
            time += instr[i].time;
            if (instr[i].type === "WaypointReached") {
                console.log("Time to waypoint: " + time);
                time = 0;
            }
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

//L.control.locate().addTo(map);

function createButton(label, container) {
    var btn = L.DomUtil.create('button', '', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}

let state = {
    campusClicked: false,
    campusFromId: null,
    campusToId: null,
    startFromThisLocationClicked: false,
    goToThisLocationClicked: false
};

function resetState() {
    state = {
        campusClicked: false,
        campusFromId: null,
        campusToId: null,
        startFromThisLocationClicked: false,
        goToThisLocationClicked: false
    };
}


map.on('click', function (e) {
    var startBtn, destBtn;
    var container = L.DomUtil.create('div');
    if ((state.startFromThisLocationClicked || state.goToThisLocationClicked) && !state.campusClicked) {
        container.appendChild(document.createElement("br"));
        let b = document.createElement("b");
        b.setAttribute('style', 'color: #cc0000');
        b.appendChild(document.createTextNode('Hi there! This is campus carpool, one of your endpoints needs to be a campus.'));
        container.appendChild(b);
        container.setAttribute('style', 'text-align: center')
    } else {
        startBtn = createButton('Start from this location', container);
        destBtn = createButton('Go to this location', container);
    }

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(map);
    L.DomEvent.on(startBtn, 'click', function () {
        if (state.goToThisLocationClicked && !state.campusClicked) {
            alert('Kies een campus!')
        }
        if (state.startFromThisLocationClicked === true) { //in case a campus was clicked before
            resetState()
        }
        state.startFromThisLocationClicked = true;
        control.spliceWaypoints(0, 1, e.latlng);
        map.closePopup();
    });

    L.DomEvent.on(destBtn, 'click', function () {
        if (state.startFromThisLocationClicked && !state.campusClicked) {
            alert('Kies een campus!')
        }
        if (state.goToThisLocationClicked === true) { //in case a campus was clicked before
            resetState()
        }
        state.goToThisLocationClicked = true;
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
    document.getElementsByClassName('leaflet-routing-geocoder')[0].remove();
    document.getElementsByClassName('leaflet-routing-add-waypoint')[0].remove();

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

                let optionChild = document.createElement('option');
                let textOption = document.createTextNode(hover_display);
                optionChild.appendChild(textOption);

                //hover_display = hover_display.substr(0, hover_display.length - 29);
                let icon = null;
                if (markers[i].category === 'university') {
                    icon = universityIcon
                } else {
                    icon = collegeIcon
                }

                (L.marker([markers[i].lat, markers[i].lng], {
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
                                offset: [0, -20]
                            })
                                .setContent(container)
                                .setLatLng(e.latlng)
                                .openOn(map);
                            setTimeout(function () {
                                map.closePopup();
                            }, 7000)
                        },
                        // 'mouseout': function (e) {
                        //     setTimeout(function () {
                        //         map.closePopup();
                        //     }, 2500)
                        // },
                        'click': function (e) {
                            let container = L.DomUtil.create('div'),
                                startBtn = createButton('Start from this location', container),
                                destBtn = createButton('Go to this location', container);
                            startBtn.setAttribute('id', this.options['id']);
                            destBtn.setAttribute('id', this.options['id']);
                            container.appendChild(document.createElement("br"));
                            container.appendChild(document.createTextNode(this.options['name']));


                            L.popup({offset: [0, -20]})
                                .setContent(container)
                                .setLatLng(e.latlng)
                                .openOn(map);
                            L.DomEvent.on(startBtn, 'click', function () {
                                state.campusClicked = true;
                                state.campusFromId = e.target['options'].id;
                                state.startFromThisLocationClicked = true;
                                control.spliceWaypoints(0, 1, e.latlng);
                                map.closePopup();
                            });

                            L.DomEvent.on(destBtn, 'click', function () {
                                state.campusClicked = true;
                                state.campusToId = e.target['options'].id;
                                state.goToThisLocationClicked = true;
                                control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
                                map.closePopup();
                            });
                        }
                    })

            }

        });

    let child = document.createElement('div');
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

    // let rbutton = document.createElement("button");
    // rbutton.innerHTML = "Do Something";
    //
    // // 2. Append somewhere
    // let rbody = document.getElementsByTagName("rbody")[0];
    // rbody.appendChild(rbutton);
    //
    // // 3. Add event handler
    // rbutton.addEventListener ("click", function() {
    //   alert("did something");
    // });
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
        var from, to;
        state.campusFromId ? from = state.campusFromId : from = control.getWaypoints()[0].latLng;
        state.campusToId ? to = state.campusToId : to = control.getWaypoints()[1].latLng;
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
                    alert("Result: " + JSON.stringify(data));
                    if (data === null) {
                        return
                    }
                    let result_div = $('#result');
                    result_div.empty();
                    result_div.attr("class", "row justify-content-center");
                    for (let d = 0; d < data["results"].length; d++) {
                        let result = data.results[d];
                        let choice = document.createElement("div");
                        choice.setAttribute("class", "border border-info rounded col-md-5 m-3");
                        let from = result.waypoints[0]["addr"];
                        let to = result.waypoints[result["len"] - 1]["addr"];
                        if (result.waypoints[0]["alias"] !== "") {
                            from += " (" + result.waypoints[0]["alias"] + ")"
                        }
                        if (result.waypoints[result["len"] - 1]["alias"] !== "") {
                            to += " (" + result.waypoints[result["len"] - 1]["alias"] + ")"
                        }
                        let innerRow = document.createElement("div");
                        innerRow.setAttribute("class", "row justify-content-center");

                        let leftColumn = document.createElement("div");
                        leftColumn.setAttribute("class", "col-md-6 text-left");

                        let rightColumn = document.createElement("div");
                        rightColumn.setAttribute("class", "col-md-6 text-left");

                        leftColumn.innerHTML = "<p class=\"my-3\"><b>From:</b> " + from + "</p>\n" +
                            "<p><b>Departure:</b> " + result["departure_time"] + "</p>\n";

                        rightColumn.innerHTML = "<p class=\"my-3\"><b>To:</b> " + to + "</p>\n" +
                            "<p><b>Arrival:</b> " + result["arrival_time"] + "</p>";

                        let underColumn = document.createElement("div");
                        underColumn.setAttribute("class", "col-md-8 text-center");

                        let mapButton = document.createElement("button");
                        mapButton.setAttribute("class", "btn btn-info m-2");
                        mapButton.innerHTML = "Show on map";

                        let addButton = document.createElement("button");
                        addButton.setAttribute("class", "btn btn-info m-2");
                        addButton.innerHTML = "Join this ride";

                        underColumn.appendChild(mapButton);
                        underColumn.appendChild(addButton);

                        innerRow.appendChild(leftColumn);
                        innerRow.appendChild(rightColumn);
                        innerRow.appendChild(underColumn);

                        choice.appendChild(innerRow);

                        result_div.append(choice);
                    }


                    // $('#result').attr("class", "row justify-content-center");
                    // for (let d = 0; d < data["results"].length; d++) {
                    //     let result = data.results[d];
                    //     let btn = document.createElement("button");
                    //     btn.setAttribute("id", "result" + d.toString())
                    //     btn.setAttribute("class","btn btn-info col-md-5 m-3 text-left");
                    //     let from, to;
                    //     if (result["to_campus"] === true) {
                    //         from = result["address_1"];
                    //         to = result["campus"];
                    //     } else {
                    //         from = result["campus"];
                    //         to = result["address_1"];
                    //     }
                    //     btn.innerHTML = "From: " + from.toString() + "<br>\n" +
                    //                     "To: " + to.toString() + "<br>\n" +
                    //                     "Departure: " + result["departure_time"] + "<br>\n" +
                    //                     "Arrival: " + result["arrival_time"] + "<br>";
                    //     $('#result').append(btn);
                    // }
                });
        }
        return false;
    });

    // insert the current date and time in the correct input field
    $('input[type="datetime-local"]').setNow();
});


/*

function Geeks() {
                var myDiv = document.getElementById("GFG");

                // creating button element
                var button = document.createElement('BUTTON');

                // creating text to be
                //displayed on button
                var text = document.createTextNode("Button");

                // appending text to button
                button.appendChild(text);

                // appending button to div
                myDiv.appendChild(button);
            }
function showcompatibleRide(){

};*/