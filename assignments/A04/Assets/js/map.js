mapboxgl.accessToken = 'pk.eyJ1Ijoia2VoaW5kZW9iYW5sYSIsImEiOiJja2ZuNm42b3kxamwzMndrdXIyNHkzOG8wIn0.qe4TrmVMMfi1Enpcvk5GfQ';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-69.0297, 7.61],
    zoom: 2,
    attributionControl: true,
    preserveDrawingBuffer: true,
});

// handles click/touch event across devices 
let touchEvent = 'ontouchstart' in window ? 'touchstart' : 'click';

// navigation controls
map.addControl(new mapboxgl.NavigationControl()); // zoom controls

// scale bar
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 90,
    unit: 'imperial',
    position: 'bottom-right'
}));

// geolocate control
map.addControl(new mapboxgl.GeolocateControl());

//This overides the Bootstrap modal "enforceFocus" to allow user interaction with main map
$.fn.modal.Constructor.prototype.enforceFocus = function() {};

// Geocoder API
// Geocoder API
// Geocoder API
var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken
});

var addressTool = document.getElementById('addressAppend');
addressTool.appendChild(geocoder.onAdd(map))
var deleteLayer = [];
map.on('load', function() {
    map.addSource('geocode-point', {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": []
        }
    });

    map.addLayer({
        "id": "geocode-point",
        "source": "geocode-point",
        "type": "circle",
        "paint": {
            "circle-radius": 20,
            "circle-color": "dodgerblue",
            'circle-opacity': 0.5,
            'circle-stroke-color': 'white',
            'circle-stroke-width': 3,
        }
    });

    geocoder.on('result', function(ev) {
        map.getSource('geocode-point').setData(ev.result.geometry);
    });

});

//Enter Lat Long
//Enter Lat Long
//Enter Lat Long

map.on('load', function() {

    $(document).ready(function() {


        //clear
        $('#findLLButtonClear').click(function() {

            map.removeLayer("enterLL");
            map.removeSource("enterLL");

            if (map.getLayer("enterLL")) {
                map.removeLayer("enterLL");
                map.removeSource("enterLL");
            }

        });

        //create
        $('#findLLButton').click(function() {

            var enterLng = +document.getElementById('lngInput').value
            var enterLat = +document.getElementById('latInput').value

            var enterLL = turf.point([enterLng, enterLat]);

            map.addSource('enterLL', {
                type: 'geojson',
                data: enterLL
            });

            map.addLayer({
                id: 'enterLL',
                type: 'circle',
                source: 'enterLL',
                layout: {

                },
                paint: {
                    "circle-color": 'red',
                    "circle-radius": 8,
                },
            });

            map.flyTo({
                center: [enterLng, enterLat]
            });

        });
    });
});
//random string generator
//random string generator
//random string generator
function makeid(length, uniqueue) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        result += uniqueue;
    }
    return result;
}
/* random color generator */
/* random color generator */
/* random color generator */
/* random color generator */
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
//enter Lat Long for nearest neghibour
//enter Lat Long for nearest neghibour
//enter Lat Long for nearest neghibour

//clear nearest neghibour lat lng
$('#findClearNearest').click(function() {
    $("#lngInputs").val('');
    $("#latInputs").val('');
    lineAnswers = document.getElementById('latlngonclick');
    lineAnswers.innerHTML = " ";


    document.getElementById("addPolygon").checked = false;

});
// find nearest and load layer
$('#findNearest').click(function() {

    var enterLng = $("#lngInputs").val()
    var enterLat = $("#latInputs").val()

    var enterLL = turf.point([enterLng, enterLat]);
    var random = 'near'
    var generate = makeid(6, random);
    paint = getRandomColor();
    deleteLayer.push(generate)
    $.getJSON("http://localhost:8080/nearestNeighbors/?lngLat=" + enterLng + "," + enterLat)
        .done(function(json) {


            map.addSource(generate, {
                'type': 'geojson',
                'data': json
                    // poly
            });
            map.addLayer({
                'id': generate,
                'source': generate,
                'type': 'circle',
                'paint': {
                    'circle-radius': 6,
                    'circle-color': paint
                }
            });
            if (document.getElementById("addPolygon").checked == true) {
                addpolygonlayer(addPolygon(json))

            }

        });

    map.flyTo({
        center: [enterLng, enterLat]
    });


});


// function to add polygon to nearest points
function addPolygon(feature) {
    var enveloped = turf.envelope(feature);
    return enveloped;
}
// adds a layer for a polygon
function addpolygonlayer(json) {
    paint = getRandomColor();
    var random = 'near'
    var generate = makeid(6, random);
    deleteLayer.push(generate)
    map.addSource(generate, {
        'type': 'geojson',
        'data': json
            // poly
    });
    map.addLayer({
        'id': generate,
        'type': 'fill',
        'source': generate,
        'paint': {
            'fill-color': paint,
            'fill-opacity': 0.9
        },
        'filter': ['==', '$type', 'Polygon']
    });

}
// draw line between two points and calc distance
// draw line between two points and calc distance
// draw line between two points and calc distance

// hides drop down menu for city A and B
$('#CitySelectA').hide();
$('#CitySelectB').hide();
// clear texbox for selected state A And B
$("#clearCity").click(function(event) {
    $("#PickCityA").val("");
    $('#CitySelectA').html("");
    $("#PickCityB").val("");
    $('#CitySelectB').html("");
    lineAnswers = document.getElementById('calculated-length2');
    lineAnswers.innerHTML = '<p>'
    '</p>';

});
// populates drop down menu for City A when search is clicked
$("#searchACity").click(function(event) {
    populateCitySelectA()
});
// populates drop down menu for City B when search is clicked
$("#searchBCity").click(function(event) {
    populateCitySelectB()
});
// when a drop down is clicked it populates the textbox with clicked value
// and hides the drop down for city A
$("#CitySelectA").click(function(event) {
    let city = $("#CitySelectA option:selected").text();
    $("#PickCityA").val(city);
    $('#CitySelectA').hide();
});
// when a drop down is clicked it populates the textbox with clicked value
// and hides the drop down for city B
$("#CitySelectB").click(function(event) {
    let city = $("#CitySelectB option:selected").text();
    $("#PickCityB").val(city);
    $('#CitySelectB').hide();
});
// check for the radio button that is clicked
//and return a clicked value
function RadioValue() {
    var ele = document.getElementsByName('units');

    for (i = 0; i < ele.length; i++) {
        if (ele[i].checked)

            return (ele[i].value);


    }
}
// on click of the submit button get the value in the
// two textboxes add a comma and the value in the radio
//button and send to flask and display length
//and add layer
$("#searchCity").click(function(event) {
    var ele = RadioValue();
    let CityA = $("#CitySelectA").val();
    let CityB = $("#CitySelectB").val();
    var message = 'fill out both cities'

    if (CityA == null || CityB == null || CityA == "" || CityB == "") {
        alert("Please Fill All Required Field");
    } else {
        var res = CityA.concat(",", CityB, ";", ele);
        var splited = CityA.split(",");
        var splited2 = CityB.split(",");
        var lng = parseFloat(splited[0]);
        var lat = parseFloat(splited[1]);
        var lng1 = parseFloat(splited2[0]);
        var lat1 = parseFloat(splited2[1]);
        $.get("http://localhost:8080/distance/?lnglat=" + res)
            .done(function(data) {

                addLayer(lng, lat, lng1, lat1)
                lineAnswers = document.getElementById('calculated-length2');
                lineAnswers.innerHTML = '<p>' + data + '</p>';
            });
    }


});
// given the long lat of both cities add a 
//layer
function addLayer(lng, lat, lng1, lat1) {
    paint = getRandomColor();
    var random = 'route'
    var generate = makeid(6, random);
    deleteLayer.push(generate)
    map.addSource(generate, {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [lng, lat],
                    [lng1, lat1]
                ]
            }
        }
    });

    map.addLayer({
        'id': generate,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint,
            'line-width': 2
        }


    });
    map.flyTo({
        center: [lng, lat],
        zoom: 3

    });
}
// read value in textbox to filter populate city A
$("#PickCityA").keyup(function(event) {
    populateCitySelectA();
});


// take the value in text box send to flask
//and display the list of cities eturned by flask
function populateCitySelectA() {
    let filter = $("#PickCityA").val();
    let html = '';
    $.get("http://localhost:8080/cities?filter=" + filter, function(data) {
        $('#CitySelectA').show();
        for (var i = 0; i < data['count']; i++) {

            html += "<option value ='" + data['results'][i].Coordinates + " '>" + data['results'][i].Name + "</option>";
        }
        $('#CitySelectA').attr("size", data['count']);
        $('#CitySelectA').html(html);

    });
}
// read value in textbox to filter populate cityB
$("#PickCityB").keyup(function(event) {
    populateCitySelectB();
});
// take the value in text box send to flask
//and display the list of cities eturned by flask
function populateCitySelectB() {
    let filter = $("#PickCityB").val();

    let html = '';
    $.get("http://localhost:8080/cities?filter=" + filter, function(data) {
        $('#CitySelectB').show();
        for (var i = 0; i < data['count']; i++) {
            html += "<option value ='" + data['results'][i].Coordinates + " '>" + data['results'][i].Name + "</option>";

        }
        $('#CitySelectB').attr("size", data['count']);
        $('#CitySelectB').html(html);

    });
}
//load city for railroads


//hide railroad dropdown
$('#stateSelectRail').hide();
//clear values in text box
$("#clearRail").click(function(event) {
    $("#pickStateRail").val("");
    $('#stateSelectRail').html("");
    getline = document.getElementById('invalidState');
    getline.innerHTML = '<p>'
    '</p>';
    getline.style.display = "none"
});
//populate states with railroad on click
$("#searchStateRail").click(function(event) {
    populateStatesSelect()
});
//on click of the drop down add the drop down value
//to the textbox and hide dropdown
$("#stateSelectRail").click(function(event) {
    let state = $("#stateSelectRail option:selected").text();
    $("#pickStateRail").val(state);
    $('#stateSelectRail').hide();
});
//search flask with the given state 
//add layer
$("#searchRail").click(function(event) {

    let state = $("#stateSelectRail").val();
    $.get("http://localhost:8080/StatesRailroad/?state=" + state)
        .done(function(data) {

            if (data['count'] == 1) {
                getline = document.getElementById('invalidState');
                getline.style.display = "block"
                getline.innerHTML = '<p>' + 'database does not contain railroad data for selected state' + '</p>';

            } else {
                addLayer1(data)
            }

        });

});
//create layer for rail road given the 
//geojson
function addLayer1(json) {
    paint = getRandomColor();
    var random = 'Rail'
    var generate = makeid(6, random);

    deleteLayer.push(generate);
    var latlng = json['geometry']['coordinates'][0];
    var enterLng = latlng[0];
    var enterLat = latlng[1];
    map.addSource(generate, {
        'type': 'geojson',
        'data': json

    });

    map.addLayer({
        'id': generate,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint,
            'line-width': 1
        }
    });
    map.flyTo({
        center: [enterLng, enterLat],
        zoom: 4
    });
}
//read user input and populate states with
//dropdown with the user input
$("#pickStateRail").keyup(function(event) {
    populateStatesSelect();
});
//populate state 
function populateStatesSelect() {
    let filter = $("#pickStateRail").val();

    let html = '';
    $.get("http://localhost:8080/states?filter=" + filter, function(data) {
        $('#stateSelectRail').show();

        for (var i = 0; i < data['count']; i++) {
            html += '<option>' + data['results'][i].name + '</option>';
        }

        $('#stateSelectRail').attr("size", data['count']);
        $('#stateSelectRail').html(html);

    });
}
/* uplaod or paste geojson */
/* uplaod or paste geojson */
/* uplaod or paste geojson */


//validate brackets
function check(expr) {
    const holder = []
    const openBrackets = ['(', '{', '[']
    const closedBrackets = [')', '}', ']']
    for (let letter of expr) { // loop trought all letters of expr
        if (openBrackets.includes(letter)) { // if its oppening bracket
            holder.push(letter)
        } else if (closedBrackets.includes(letter)) { // if its closing
            const openPair = openBrackets[closedBrackets.indexOf(letter)] // find his pair
            if (holder[holder.length - 1] === openPair) { // check if that pair is last element in array
                holder.splice(-1, 1) //if so, remove it
            } else { // if its not
                holder.push(letter)
                break // exit loop
            }
        }
    }
    return (holder.length === 0) // return true if length is 0, otherwise false
}
// takes a string array and convert to a float array
function convert(str) {
    list = [];
    ConvertedString = [];
    //splits by [];
    res = str.split(/(\[.*?\])/).filter(Boolean);
    // checks if an index is not whitspace or comma
    // and adds it to an aray
    for (i = 0; i < res.length; i++) {
        var thing = res[i].trim();
        if (thing != ',') {

            if (/\S/.test(thing)) {
                list.push(thing);

            }

        }
    }
    console.log(list);
    //converts  a string array to float
    for (i = 0; i < list.length; i++) {
        array = list[i].match(/-?\d+(?:\.\d+)?/g).map(Number);
        ConvertedString.push(array);
    }
    return ConvertedString;
}
//onclick call addeojsonlayer
$("#loadmap").click(function(event) {
    var Coordinate = $("#TexrareaGeo").val();
    var featureValue = $("#featureType").val();
    var checked = featureValue.toLowerCase();

    if (Coordinate == null || featureValue == null || Coordinate == "" || featureValue == "") {
        alert("Please Fill All Required Field");
    } else {
        if (check(Coordinate)) {
            var answer = convert(Coordinate)
            console.log(answer[0]);
            //call back end
            $.get("http://localhost:8080/CreateFeature/?value=" + JSON.stringify(answer) + ";" + featureValue)
                .done(function(data) {

                    if (checked == "polygon") {

                        createpastedLayerPolygon(data, answer[0])
                    } else if (checked == "linestring" || checked == "multilinestring") {
                        createpastedLayerLinsString(data, answer[0])

                    } else {

                        createpastedLayerPoints(data, answer[0])
                    }
                    // add download button

                });

        } else {
            getline = document.getElementById('invalidGeojson');
            getline.style.display = "block"
            getline.innerHTML = '<p>' + 'Coordinates are missing some  brackets' + '</p>';
        }


    }
});

/* add layerfor pasted geojson for points */
/* add layerfor pasted geojson for points */
/* add layerfor pasted geojson for points */
function createpastedLayerPoints(json, flytocoords) {
    paint = getRandomColor();
    var random = 'Geo'
    var generate = makeid(6, random);
    deleteLayer.push(generate);
    map.addSource(generate, {
        'type': 'geojson',
        'data': json
            // poly
    });
    map.addLayer({
        'id': generate,
        'source': generate,
        'type': 'circle',
        'paint': {
            'circle-radius': 6,
            'circle-color': paint
        }
    });
    map.flyTo({
        center: flytocoords,
        zoom: 5,
    });


}

/* add layerfor pasted geojson for polygon*/
/* add layerfor pasted geojson for polygon*/
/* add layerfor pasted geojson for polygon*/
function createpastedLayerPolygon(json, flytocoords) {
    paint = getRandomColor();
    var random = 'Geo'
    var generate = makeid(6, random);
    deleteLayer.push(generate);
    map.addSource(generate, {
        'type': 'geojson',
        'data': json
            // poly
    });
    map.addLayer({
        'id': generate,
        'type': 'fill',
        'source': generate,
        'paint': {
            'fill-color': paint,
            'fill-opacity': 0.2
        },
        'filter': ['==', '$type', 'Polygon']
    });
    map.flyTo({
        center: flytocoords,
        zoom: 4,
    });


}
/* add layerfor pasted geojson for lineString*/
/* add layerfor pasted geojson for lineString*/
/* add layerfor pasted geojson for lineString*/
function createpastedLayerLinsString(json, flytocoords) {
    paint = getRandomColor();
    var random = 'Geo'
    var generate = makeid(6, random);
    deleteLayer.push(generate);
    map.addSource(generate, {
        'type': 'geojson',
        'data': json
            // poly
    });
    map.addLayer({
        'id': generate,
        'type': 'line',
        'source': generate,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': paint,
            'line-width': 5
        }
    });
    map.flyTo({
        center: flytocoords,
        zoom: 15,
    });


}

//clear textbox for pasted geojson
$("#clearpasted").click(function(event) {
    $("#TexrareaGeo").val("");
    $("#featureType").val("");
    getline = document.getElementById('invalidGeojson');
    getline.innerHTML = '<p>'
    '</p>';
    getline.style.display = "none"

});



// Start file download.

// function downloadObjectAsJson(exportObj, exportName) {
//     var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj));

//     var downloadAnchorNode = document.createElement('a');
//     downloadAnchorNode.setAttribute("href", dataStr);
//     downloadAnchorNode.setAttribute('download', exportName + ".geojson ");
//     downloadAnchorNode.style.display = 'none';
//     document.body.appendChild(downloadAnchorNode); // required for firefox
//     downloadAnchorNode.click();
//     downloadAnchorNode.remove();
// }
// Start file download.


function getSelectedCheckboxValues(boxs) {
    const checkboxes = document.querySelectorAll(`input[name="${boxs}"]:checked`);

    let values = [];
    checkboxes.forEach((checkbox) => {

        values.push(checkbox.value);
    });

    return values;
}

const btn = document.querySelector('#buttondelete');
btn.addEventListener('click', (event) => {
    var list = [];
    list = getSelectedCheckboxValues('boxs')
    list.forEach(removelayers);


});
const btns = document.querySelector('#clearcheckbox');
btns.addEventListener('click', (event) => {
    var list = [];
    list = getSelectedCheckboxValues('boxs')
    for (i = 0; i < list.length; i++) {
        document.getElementById(list[i]).checked = false;
    }

});



//to remove layers
function removelayers(layer) {
    var afterdellete = []
    for (i = 0; i < deleteLayer.length; i++) {
        var contain = deleteLayer[i];

        if (contain.includes(layer)) {
            afterdellete.push(contain);
            map.removeLayer(contain);
            map.removeSource(contain);
        }
    }

    for (i = 0; i < afterdellete.length; i++) {
        if (deleteLayer.includes(afterdellete[i])) {
            const index = deleteLayer.indexOf(afterdellete[i]);
            deleteLayer.splice(index, 1)
        }
    }
}
//draw tool
var drawmodal = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});
var drawTools = document.getElementById('drawAppends');
drawTools.appendChild(drawmodal.onAdd(map)).setAttribute("style", "display: inline-flex;", "border: 0;");
map.on('draw.create', updateArea);



function updateArea(e) {
    paint = getRandomColor();
    var data = drawmodal.getAll();
    var coords = turf.meta.coordAll(data);
    var line = turf.lineString(coords);
    var bbox = turf.bbox(line);
    var random = 'DrawL'
    var generate = makeid(6, random);

    deleteLayer.push(generate);
    var poly = turf.bboxPolygon(bbox);

    boundingBoxPolygon(poly)
    $.getJSON("http://localhost:8080/interSection/?lngLat=" + bbox)
        .done(function(json) {
            map.addSource(generate, {
                'type': 'geojson',
                'data': json
                    // poly
            });
            map.addLayer({
                'id': generate,
                'source': generate,
                'type': 'circle',
                'paint': {
                    'circle-radius': 6,
                    'circle-color': paint
                }
            });


        })



}

function boundingBoxPolygon(polygonfeature) {
    paint = getRandomColor();
    var random = 'DrawL'
    var generate = makeid(6, random);
    deleteLayer.push(generate);
    map.addSource(generate, {
        'type': 'geojson',
        'data': polygonfeature
            // poly
    });
    map.addLayer({
        'id': generate,
        'type': 'fill',
        'source': generate,
        'paint': {
            'fill-color': paint,
            'fill-opacity': 0.4
        },
        'filter': ['==', '$type', 'Polygon']
    });
}


// Coordinates Tool
// Coordinates Tool
// Coordinates Tool
map.on(touchEvent, function(e) {
    var json = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinate": [e.lngLat.toArray()]
        },
        "properties": {

        }

    };
    latlngonclick
    document.getElementById('info').innerHTML =
        JSON.stringify(e.lngLat, function(key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
    document.getElementById('latlngonclick').innerHTML =
        JSON.stringify(e.lngLat, function(key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
        // create json to store
        // create json to store
        // create json to store

});

//BOOKMARKS
//BOOKMARKS
//BOOKMARKS

document.getElementById('icelandBookmark').addEventListener('click', function() {
    map.flyTo({
        center: [-18.7457, 65.0662],
        zoom: 5,
    });
});

document.getElementById('safricaBookmark').addEventListener('click', function() {

    map.flyTo({
        center: [23.9417, -29.5353],
        zoom: 5,
    });
});

document.getElementById('japanBookmark').addEventListener('click', function() {

    map.flyTo({
        center: [138.6098, 36.3223],
        zoom: 4,
    });
});

document.getElementById('australiaBookmark').addEventListener('click', function() {

    map.flyTo({
        center: [134.1673, -25.6855],
        zoom: 3

    });
});