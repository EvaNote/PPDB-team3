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
    serviceUrl: 'http://35.195.213.223:69/route/v1',
    routeWhileDragging: true,
    draggableWaypoints: false,
    geocoder: L.Control.Geocoder.nominatim(),
    addWaypoints: false,
    createMarker: function (i, wp) {
        return L.marker(wp.latLng).on('mouseover', function (e) {
            var msg, changeOrderBtn, removeWaypointBtn;
            var container = L.DomUtil.create('div');
            if (e.latlng === state.startFromThisLocationClicked) {
                msg = 'start point';
                container.appendChild(document.createTextNode(msg));
            } else if (e.latlng === state.goToThisLocationClicked) {
                msg = 'end point';
                container.appendChild(document.createTextNode(msg));
            } else if (e.latlng === state.p1) {
                msg = 'pickup point 1';
                if (state.p2 !== null) {
                    changeOrderBtn = createButton('Change order...', container);
                }
                removeWaypointBtn = createButton('Remove this waypoint', container);
                container.appendChild(document.createElement("br"));
                container.appendChild(document.createTextNode(msg));
            } else if (e.latlng === state.p2) {
                msg = 'pickup point 2';
                removeWaypointBtn = createButton('Remove this waypoint', container);
                changeOrderBtn = createButton('Change order...', container);
                container.appendChild(document.createElement("br"));
                container.appendChild(document.createTextNode(msg));
            } else {
                msg = 'pickup point 3';
                removeWaypointBtn = createButton('Remove this waypoint', container);
                changeOrderBtn = createButton('Change order...', container);
                container.appendChild(document.createElement("br"));
                container.appendChild(document.createTextNode(msg));
            }
            container.setAttribute('style', 'text-align: center')

            L.popup({
                offset: [0, -20]
            })
                .setContent(container)
                .setLatLng(e.latlng)
                .openOn(map);
            setTimeout(function () {
                map.closePopup();
            }, 15000);

            L.DomEvent.on(removeWaypointBtn, 'click', function () {
                let waypoints = control.getWaypoints();
                var i;
                if (e.latlng === state.p1) {
                    i = 1;
                    state.p1 = state.p2;
                    state.p2 = state.p3;
                } else if (e.latlng === state.p2) {
                    i = 2;
                    state.p2 = state.p3;
                } else {
                    i = 3;
                }
                waypoints.splice(i, 1);
                control.setWaypoints(waypoints);
            });

            L.DomEvent.on(changeOrderBtn, 'click', function () {
                var btn1;
                var btn2;
                var btn3;
                var container = L.DomUtil.create('div');

                if (e.latlng === state.p1) {
                    btn2 = createButton('2', container);
                    btn2.setAttribute('id', 'id_1_2');
                    if (state.p3 !== null) {
                        btn3 = createButton('3', container);
                        btn3.setAttribute('id', 'id_1_3');
                    }
                } else if (e.latlng === state.p2) {
                    btn1 = createButton('1', container);
                    btn1.setAttribute('id', 'id_2_1');
                    if (state.p3 !== null) {
                        btn3 = createButton('3', container);
                        btn3.setAttribute('id', 'id_2_3');
                    }
                } else {
                    btn1 = createButton('1', container);
                    btn1.setAttribute('id', 'id_3_1');
                    btn2 = createButton('2', container);
                    btn2.setAttribute('id', 'id_3_2');
                }

                container.setAttribute('style', 'text-align: center');

                map.closePopup();

                L.popup({
                    offset: [0, -20]
                })
                    .setContent(container)
                    .setLatLng(e.latlng)
                    .openOn(map);

                $('#id_1_2').on('click', function () {
                    //swap index 1 with index 2
                    let temp = state.p1;
                    state.p1 = state.p2;
                    state.p2 = temp;
                    let waypoints = control.getWaypoints();
                    waypoints[1] = state.p1;
                    waypoints[2] = state.p2;
                    control.setWaypoints(waypoints)
                });

                $('#id_2_1').on('click', function () {
                    //swap index 1 with index 2
                    let temp = state.p1;
                    state.p1 = state.p2;
                    state.p2 = temp;
                    let waypoints = control.getWaypoints();
                    waypoints[1] = state.p1;
                    waypoints[2] = state.p2;
                    control.setWaypoints(waypoints)
                });

                $('#id_3_1').on('click', function () {
                    let temp = state.p1;
                    state.p1 = state.p3;
                    state.p3 = temp;
                    let waypoints = control.getWaypoints();
                    waypoints[1] = state.p1;
                    waypoints[3] = state.p3;
                    control.setWaypoints(waypoints)
                })

                $('#id_1_3').on('click', function () {
                    let temp = state.p1;
                    state.p1 = state.p3;
                    state.p3 = temp;
                    let waypoints = control.getWaypoints();
                    waypoints[1] = state.p1;
                    waypoints[3] = state.p3;
                    control.setWaypoints(waypoints)
                })

                $('#id_2_3').on('click', function () {
                    let temp = state.p2;
                    state.p2 = state.p3;
                    state.p3 = temp;
                    let waypoints = control.getWaypoints();
                    waypoints[2] = state.p2;
                    waypoints[3] = state.p3;
                    control.setWaypoints(waypoints)
                })

                $('#id_3_2').on('click', function () {
                    let temp = state.p2;
                    state.p2 = state.p3;
                    state.p3 = temp;
                    let waypoints = control.getWaypoints();
                    waypoints[2] = state.p2;
                    waypoints[3] = state.p3;
                    control.setWaypoints(waypoints)
                })
            });
        });
    }
}).addTo(map);

//L.control.locate().addTo(map);

function createButton(label, container) {
    var btn = L.DomUtil.create('button', '', container);
    btn.setAttribute('type', 'button');
    btn.innerHTML = label;
    return btn;
}

let state = {
    situation: null,
    campusClicked: false,
    campusFromId: null,
    campusToId: null,
    startFromThisLocationClicked: null,
    goToThisLocationClicked: null,
    p1: null,
    p2: null,
    p3: null
};

function resetState() {
    state = {  // do not reset situation
        campusClicked: false,
        campusFromId: null,
        campusToId: null,
        startFromThisLocationClicked: null,
        goToThisLocationClicked: null,
        p1: null,
        p2: null,
        p3: null
    };
}

map.on('click', function (e) {
    var startBtn, destBtn, addWaypointBtn;
    var container = L.DomUtil.create('div');
    console.log(state);
    if (state.startFromThisLocationClicked && state.goToThisLocationClicked && state.situation === 'create') {
        if (state.p3 !== null) {
            container.appendChild(document.createElement("br"));
            let b = document.createElement("b");
            b.setAttribute('style', 'color: #cc0000');
            b.appendChild(document.createTextNode('Hi there! You can\'t indicate more than three pickup points.'));
            container.appendChild(b);
            container.setAttribute('style', 'text-align: center')
        } else {
            startBtn = createButton('Add this point as pickup point', container);
            startBtn.setAttribute('id', 'pickup')
        }
    } else if ((state.startFromThisLocationClicked || state.goToThisLocationClicked) && !state.campusClicked) {
        container.appendChild(document.createElement("br"));
        let b = document.createElement("b");
        b.setAttribute('style', 'color: #cc0000');
        b.appendChild(document.createTextNode('Hi there! This is campus carpool, one of your endpoints needs to be a campus.'));
        container.appendChild(b);
        if (state.startFromThisLocationClicked) {
            startBtn = createButton('Start from this location instead', container);
        } else {
            destBtn = createButton('Go to this location instead', container);
        }
        container.setAttribute('style', 'text-align: center')
    } else {
        startBtn = createButton('Start from this location', container);
        startBtn.setAttribute('id', 'start');
        destBtn = createButton('Go to this location', container);
    }

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(map);

    L.DomEvent.on(startBtn, 'click', function () {
        if (startBtn.getAttribute('id') === 'start') {
            // case 1: state.startFromThisLocationClicked === true && campusFromId !== nul
            if (state.startFromThisLocationClicked !== null && state.campusFromId !== null) { //in case a campus was clicked before
                resetState()  // to location is not chosen yet so safely reset
            }
            // case 2: state.startFromThisLocationClicked === true && campusFromId === nul
            // does not require any action
            state.startFromThisLocationClicked = e.latlng;
            map.closePopup();
            control.spliceWaypoints(0, 1, e.latlng);
        } else {
            if (state.p1 === null) {
                state.p1 = e.latlng;
                control.spliceWaypoints(1, 0, e.latlng);
            } else if (state.p2 === null) {
                state.p2 = e.latlng;
                control.spliceWaypoints(2, 0, e.latlng);
            } else {
                state.p3 = e.latlng;
                control.spliceWaypoints(3, 0, e.latlng);
            }
        map.closePopup();
            control.spliceWaypoints(1, 0, e.latlng);
        }
    });

    L.DomEvent.on(destBtn, 'click', function () {
        // case 1: state.goToThisLocationClicked === true && campusToId !== nul
        if (state.goToThisLocationClicked !== false && state.campusToId !== null) { //in case a campus was clicked before
            resetState()  // to location is not chosen yet so safely reset
        }
        // case 2: state.goToThisLocationClicked === true && campusToId === nul
        // does not require any action
        state.goToThisLocationClicked = e.latlng;
        map.closePopup();
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
    });
});


/**************
 * jQuery functions
 * ************/

$(document).ready(function () {

    //TODO: dropdown? Lijst? Niks?
    document.getElementsByClassName('leaflet-routing-geocoder')[1].remove();
    document.getElementsByClassName('leaflet-routing-geocoder')[0].remove();
    //document.getElementsByClassName('leaflet-routing-add-waypoint')[0].remove();

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
                            }, 15000)
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
                                state.startFromThisLocationClicked = e.latlng;
                                control.spliceWaypoints(0, 1, e.latlng);
                                map.closePopup();
                            });

                            L.DomEvent.on(destBtn, 'click', function () {
                                state.campusClicked = true;
                                state.campusToId = e.target['options'].id;
                                state.goToThisLocationClicked = e.latlng;
                                control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
                                map.closePopup();
                            });
                        }
                    })

            }

        });

    let child = document.createElement('div');
    let temp = "<form action=\"#\" id=\"ride-time\">\n" +
        "    <label for=\"time_option\">\n<select name=\"time_option\">\n" +
        "        <option>Arrive by</option>\n" +
        "        <option>Depart at</option>\n" +
        "    </select>\n" +
        "        <input id=\"time_input\" type=\"datetime-local\" name=\"datetime\">\n" +
        "    </label>\n"
    let el = document.getElementById('create_ride');
    if (el !== null) {
        state.situation = 'create'
    } else {
        state.situation = 'find'
    }

    if (state.situation === 'create') {
        console.log(el);
        temp += "    <label for=\"passengers\">Available passenger seats:\n" +
            "    <input type=\"number\" id=\"passengers\" name=\"passengers\" value=\"0\" required style='width: 30px'>\n<br>" +
            "    </label>\n";
    }
    temp +=
        "    <input type=\"submit\" value=\"Submit\">\n" +
        "</form>";
    child.innerHTML = temp;
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
        var points = control.getWaypoints().length;
        state.campusToId ? to = state.campusToId : to = control.getWaypoints()[points-1].latLng;

        let form = $('form').serializeObject();
        let time_option = form.time_option;
        var arrive_time;
        var depart_time;

        let instr = control._line._route.instructions;
        let time = 0;
        var times = [];
        for (let i in instr) {
            time += instr[i].time;
            if (instr[i].type === "WaypointReached") {
                //console.log("Time to waypoint: " + time);
                times.push(time);
                time = 0;
            }
            if (instr[i].type === "DestinationReached"){
                //alert("ka");
                times.push(time);
                time = 0;
            }
        }
        let seconds = times[times.length-1];
        arrive_time = new Date(form.datetime.replace('T', ' ') + ":00");
        depart_time = new Date(form.datetime.replace('T', ' ') + ":00");
        var arrive = true;
        if (time_option === "Arrive by"){
            depart_time.setSeconds( depart_time.getSeconds() - seconds );
            //alert("wiewa arrive")
        }
        if (time_option === "Depart at"){
            arrive_time.setSeconds(arrive_time.getSeconds() + seconds);
            //alert("wiewa depart")
            arrive = false;
        }
        var pickup_points = [];
        var estimated_times = [];
        if (points > 2){
            var pickup = control.getWaypoints()[1].latLng;
            pickup_points.push(pickup);
            var estimated_time = new Date(form.datetime.replace('T', ' ') + ":00");
            if (arrive){
                estimated_time.setSeconds(arrive_time.getSeconds() - times[0]);
            }
            else{
                estimated_time.setSeconds(depart_time.getSeconds() + times[0]);
            }
            estimated_times.push(estimated_time);
            if (points > 3){
                var pickup2 = control.getWaypoints()[2].latLng;
                pickup_points.push(pickup2);
                var estimated_time2 = new Date(form.datetime.replace('T', ' ') + ":00");
                if (arrive){
                    estimated_time2.setSeconds(arrive_time.getSeconds() - times[1]);
                }
                else{
                    estimated_time2.setSeconds(depart_time.getSeconds() + times[1]);
                }
                estimated_times.push(estimated_time2);
                if (points > 4){
                    var pickup3 = control.getWaypoints()[3].latLng;
                    pickup_points.push(pickup3);
                    var estimated_time3 = new Date(form.datetime.replace('T', ' ') + ":00");
                    if (arrive){
                        estimated_time3.setSeconds(arrive_time.getSeconds() - times[2]);
                    }
                    else{
                        estimated_time3.setSeconds(depart_time.getSeconds() + times[2]);
                    }
                    estimated_times.push(estimated_time3);
                }
            }
        }

        for (let i in estimated_times){
            time = estimated_times[i];
            //alert("estimated time voor omzet:" + time);
            estimated_times[i] = time.toISOString().split('T')[0]+' '+time.toTimeString().split(' ')[0];
            //alert("estimated time na omzet:" + estimated_times[i]);
        }

        //alert(estimated_times);
        // check if from-to are defined. If they aren't, nothing should happen
        if (typeof from !== 'undefined' && typeof to !== 'undefined') {
            var e = document.getElementById("ride_option");
            let el = document.getElementById('create_ride');
            let ride_option = state.situation;
            if (ride_option === "create") {
                $.post({
                    contentType: "application/json",
                    url: "/en/createRide",
                    data: JSON.stringify({from: from, to: to, arrive_time: arrive_time.toMysqlFormat(),
                        depart_time: depart_time.toMysqlFormat(),
                        passengers: form.passengers, pickup_points: pickup_points, estimated_times: estimated_times})
                })
                    // when post request is done, get the returned data and do something with it
                    .done(function (data) { // response function
                        //alert("CREATE: " + JSON.stringify(data));
                        alert("Created a new ride. You can see, edit and delete your created rides on the 'My Rides' page.")
                    });

            }
            if (ride_option === "find") {
                let start = new Date();
                $.post({
                    contentType: "application/json",
                    url: "/en/calculateCompatibleRides",
                    data: JSON.stringify({from: from, to: to, time_option: form.time_option, datetime: form.datetime})
                })
                    // when post request is done, get the returned data and do something with it
                    .done(function (data) { // response function
                        ride_count = data["results"].length
                        alert("Found " + ride_count + " matches! Scroll down to see them.");
                        //alert("FIND: " + JSON.stringify(data));
                        if (data === null) {
                            return
                        }
                        let result_div = $('#result');
                        result_div.empty();
                        result_div.attr("class", "row justify-content-center");
                        for (let d = 0; d < data["results"].length; d++) {
                            let stop = new Date();
                            console.log(stop - start);
                            let result = data.results[d];
                            let driver = data["drivers"][d]
                            let driver_name = driver["first_name"] + " " + driver["last_name"]
                            let choice = document.createElement("div");
                            choice.setAttribute("class", "border border-info rounded col-md-5 m-3 text-left");
                            console.log(result);
                            let from = result.waypoints[0]["addr"];
                            let to = result.waypoints[result["len"] - 1]["addr"];
                            if (result.waypoints[0]["alias"] !== "") {
                                from += " (" + result.waypoints[0]["alias"] + ")"
                            }
                            if (result.waypoints[result["len"] - 1]["alias"] !== "") {
                                to += " (" + result.waypoints[result["len"] - 1]["alias"] + ")"
                            }
                            let innerRow = document.createElement("div");
                            innerRow.setAttribute("class", "row");

                            let leftColumn = document.createElement("div");
                            leftColumn.setAttribute("class", "col-md-6 text-left");

                            let rightColumn = document.createElement("div");
                            rightColumn.setAttribute("class", "col-md-6 text-left");

                            leftColumn.innerHTML = "<p class=\"my-3\"><b>From:</b> " + from + "</p>\n" +
                                "<p><b>Departure:</b> " + result["departure_time"] + "</p>\n"  +
                                "<p><b>Driver:</b> " + driver_name + "</p>\n";

                            rightColumn.innerHTML = "<p class=\"my-3\"><b>To:</b> " + to + "</p>\n" +
                                "<p><b>Arrival:</b> " + result["arrival_time"] + "</p>\n";

                            let underColumn = document.createElement("div");
                            underColumn.setAttribute("class", "col-md-8 text-center");

                            let mapButton = document.createElement("button");
                            mapButton.setAttribute("class", "btn btn-info m-2");
                            mapButton.onclick = function() {
                                //beginCoords  find the closest maybe pickupPoint
                                let results = data.results[d];
                                let tempArr = [];
                                let n = results.closest;
                                while(n<results.len){
                                    if(results.waypoints[n] != null){
                                        tempArr.push(L.latLng(results.waypoints[n].lat, results.waypoints[n].lng))
                                    }
                                    n++;
                                }
                                map.removeControl(control);
                                control = L.Routing.control({
                                    serviceUrl: 'http://127.0.0.1:5001/route/v1',
                                    waypoints: tempArr,
                                    autoRoute: true,
                                }).addTo(map);
                            }
                            mapButton.innerHTML = "Show on map";


                            let addButton = document.createElement("button");
                            addButton.setAttribute("class", "btn btn-info m-2");
                            addButton.setAttribute("id", "ride-button-" + d.toString());
                            addButton.innerHTML = "Join this ride";
                            addButton.addEventListener("click", function() {
                                $.post({
                                    contentType: "application/json",
                                    url: "/en/joinride",
                                    data: JSON.stringify({ride_id: result.id})
                                })
                                    // when post request is done, get the returned data and do something with it
                                    .done(function (data2) {
                                        if(data2){
                                            if (data2["result"] === "success") {
                                                alert("Ride joined successfully.")
                                            } else {
                                                alert("You already joined this ride.")
                                            }
                                        }
                                    });
                            } )
                            let driverButton = document.createElement("button");
                            driverButton.setAttribute("class", "btn btn-info m-2");
                            driverButton.innerHTML = "See driver profile";
                            let driver_id = driver["id"];
                            driverButton.onclick = function() {
                                let current_url = window.location.href;
                                let new_url = current_url.substring(0,current_url.length-8);
                                new_url += "user=" + driver_id;
                                window.open(new_url,"_blank");
                                }
                            underColumn.appendChild(mapButton);
                            underColumn.appendChild(addButton);
                            underColumn.appendChild(driverButton)

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
        }
        return false;
    });

    // insert the current date and time in the correct input field
    $('input[type="datetime-local"]').setNow();
});


// src https://stackoverflow.com/questions/5129624/convert-js-date-time-to-mysql-datetime/11150727#11150727
/**
 * You first need to create a formatting function to pad numbers to two digits…
 **/
function twoDigits(d) {
    if(0 <= d && d < 10) return "0" + d.toString();
    if(-10 < d && d < 0) return "-0" + (-1*d).toString();
    return d.toString();
}

/**
 * …and then create the method to output the date string as desired.
 * Some people hate using prototypes this way, but if you are going
 * to apply this to more than one Date object, having it as a prototype
 * makes sense.
 **/
Date.prototype.toMysqlFormat = function() {
    return this.getUTCFullYear() + "-" + twoDigits(1 + this.getUTCMonth()) + "-" + twoDigits(this.getUTCDate()) + " " + twoDigits(this.getUTCHours()+2) + ":" + twoDigits(this.getUTCMinutes()) + ":" + twoDigits(this.getUTCSeconds());
};

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
