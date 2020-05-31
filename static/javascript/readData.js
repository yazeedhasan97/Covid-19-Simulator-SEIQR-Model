var name_array = [];
var lat_array = [];
var lng_array = [];
var cont_array = [];
var iso_array = [];
var pop_array = [];
var heatMapData = [];
var jordan = new google.maps.LatLng(31.25, 37);
var map;
var heatmap;
function read_data() {
    jQuery.get('http://localhost/polls/static/files/finals.txt',function(data){
        var lines = data.split(/\r\n|\n/g);
        for (var i = 0; i < lines.length; i++) {
            line = lines[i].split(/\s+/g);
            name_array.push(line[0]);
            lat_array.push(line[1]);
            lng_array.push(line[2]);
            cont_array.push(line[3]);
            iso_array.push(line[4]);
            pop_array.push(line[5]);
        }
        console.log(name_array);
        console.log(lat_array);
        console.log(lng_array);
        console.log(cont_array);
        console.log(iso_array);
        console.log(pop_array);
    });
    for (var i = 0; i < name_array.length; i++) {
        heatMapData.push({location: new google.maps.LatLng(lat_array[i], lng_array[i]), weight: pop_array[i]});
    }
    map = new google.maps.Map(document.getElementById('hmaps'), {
      center: jordan,
      zoom: 7
    //  mapTypeId: 'satellite'
    });
    heatmap = new google.maps.visualization.HeatmapLayer({
      data: heatMapData
    });
    heatmap.setMap(map);
}