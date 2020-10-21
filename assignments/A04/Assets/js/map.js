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
function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}
//enter Lat Long for nearest neghibour
//enter Lat Long for nearest neghibour
//enter Lat Long for nearest neghibour

//clear nearest neghibour lat lng
$('#findClearNearest').click(function() {
    $("#lngInputs").val('')
    $("#latInputs").val('')

});
// find nearest and load layer
$('#findNearest').click(function() {

    var enterLng = $("#lngInputs").val()
    var enterLat = $("#latInputs").val()

    var enterLL = turf.point([enterLng, enterLat]);
    var generate = 'near'
    var random = makeid(6);
    generate = generate + random;
    $.getJSON("http://localhost:8080/click/?lngLat=" + enterLng + "," + enterLat)
        .done(function(json) {
            console.log(json)

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
                    'circle-color': '#B42222'
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
    var generate = 'MAP'
    var random = makeid(6);
    generate = generate + random;
    console.log(json);
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
            'fill-color': '#0a0a0a',
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
    console.log(CityA);
    console.log(CityB);
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
                console.log(data)
                addLayer(lng, lat, lng1, lat1)
                lineAnswers = document.getElementById('calculated-length2');
                lineAnswers.innerHTML = '<p>' + data + '</p>';
            });
    }


});
// given the long lat of both cities add a 
//layer
function addLayer(lng, lat, lng1, lat1) {
    var generate = 'route'
    var random = makeid(6);
    generate = generate + random;
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
            'line-color': '#fcba03',
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
    var generate = 'Rail'
    var random = makeid(6);
    generate = generate + random;
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
            'line-color': '#4103fc',
            'line-width': 1
        }
    });
    map.flyTo({
        center: [enterLng, enterLat],
        zoom: 2
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

/* add layerfor pasted geojson */
/* add layerfor pasted geojson */
/* add layerfor pasted geojson */
function AddpastedGeojsonlayer(json) {
    var generate = 'Geo'
    var random = makeid(6);
    generate = generate + random;
    deleteLayer.push(generate);
    console.log(json);
    // var latlng = json['geometry']['coordinates'][0];
    // var enterLng = latlng[0];
    // var enterLat = latlng[1];
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
            'line-color': '#FF0000',
            'line-width': 1
        }
    });
    // map.flyTo({
    //     center: [enterLng, enterLat],
    //     zoom: 4
    // });
}
//onclick call addeojsonlayer
$("#loadmap").click(function(event) {
    if ($.trim($("#TexrareaGeo").val())) {
        let data = $("#TexrareaGeo").val();
        err = "invalid geojson object"
        if (AddpastedGeojsonlayer(data) == err) {
            getline = document.getElementById('invalidGeojson');
            getline.style.display = "block"
            getline.innerHTML = '<p>' + 'invalid geojson' + '</p>';

        } else {
            AddpastedGeojsonlayer(data);
        }
    }
});
//clear textbox
$("#clearpasted").click(function(event) {
    $("#TexrareaGeo").val("");

});

function getSelectedCheckboxValues(boxs) {
    const checkboxes = document.querySelectorAll(`input[name="${boxs}"]:checked`);

    let values = [];
    checkboxes.forEach((checkbox) => {
        console.log(checkbox);
        values.push(checkbox.value);
    });

    return values;
}

const btn = document.querySelector('#buttondelete');
btn.addEventListener('click', (event) => {
    var list = [];
    list = getSelectedCheckboxValues('boxs')

    list.forEach(removelayer);

});

function esting(list) {
    for (i = 0; i < list.length; i++) {
        removelayer(list[i]);
    }

}

//to remove layers
function removelayer(layer) {

    var afterdellete = []
    for (i = 0; i < deleteLayer.length; i++) {
        var contain = deleteLayer[i];
        console.log(contain);
        if (contain.includes(layer)) {
            afterdellete.push(contain);
            map.removeLayer(contain);
            map.removeSource(contain);
        }
    }
    for (i = 0; i < afterdellete.length; i++) {
        console.log("tried to delete");
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
    var data = drawmodal.getAll();

    var coords = turf.meta.coordAll(data);
    console.log(coords);
    var line = turf.lineString(coords);
    var bbox = turf.bbox(line);
    var generate = 'DrawL'
    var random = makeid(6);
    generate = generate + random;
    deleteLayer.push(generate);

    $.getJSON("http://localhost:8080/interSection/?lngLat=" + bbox)
        .done(function(json) {
            console.log(json)
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
                    'circle-color': '#f803fc'
                }
            });


        })



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
    console.log(json)
    document.getElementById('info').innerHTML =
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