/*****  How to send data from JavaScript to Python  *****
 *
 * make an AJAX post request with jQuery with some data and a response function. This post request will
 * post to a new Flask route, which will do some stuff with that data and then return something.
 * The returned data from the Flask route can be retrieved by the response function we put after the
 * post request.
 */
// document.getElementById("theButton").onclick = function doWork() {
//     // ajax the JSON to the server
//     $.post("/en/receiver", {lat: 4.3, lon: 51}) // data to post
//         .done(function (data) { // response function
//             alert("Data Loaded: " + data);
//         });
// };
//
// // in a certain routes.py file:
// @main.route('/receiver', methods=['POST'])
// def receiver():
//     # read json + reply
//     lat = float(request.form['lat'])
//     lon = float(request.form['lon'])
//     result = "latitude = {} and longitude = {}".format(lat, lon)
//     return result
/** END **/


// make a map that will be placed on the 'Find my ride' page
let map = L.map('findride_map').setView([51, 4.4], 10);

// add a tile layer to the (empty) map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// when someone clicks on the map, we show a popup with the coordinates of that spot
map.on('click', function onMapClick(e) {
    let popup = L.popup();
    popup.setLatLng(e.latlng).setContent("You clicked the map at " + e.latlng.toString()).openOn(map);
});

// // try to locate the user using his location service
// map.locate({setView: true, maxZoom: 16});

// // if user location was found, show a radius around the user with a popup,
// // which shows the accuracy of the localization
// map.on('locationfound', function onLocationFound(e) {
//     let radius = e.accuracy;
//     L.marker(e.latlng).addTo(map).bindPopup("You are within " + radius + " meters from this point").openPopup();
//     L.circle(e.latlng, radius).addTo(map);
// });

// // if user localization failed, show an error alert
// map.on('locationerror', function onLocationError(e) {
//     alert(e.message);
// });

// add OSRM support using Leaflet Routing Machine
L.Routing.control({
    serviceUrl: 'http://127.0.0.1:5001/route/v1',
    routeWhileDragging: true,
    geocoder: L.Control.Geocoder.nominatim()
}).on('routesfound', function (e) {

}).addTo(map);
