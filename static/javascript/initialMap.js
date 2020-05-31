var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('gmaps'), {
        center: {lat: 31.25, lng: 37},
        zoom: 7
    });
}
