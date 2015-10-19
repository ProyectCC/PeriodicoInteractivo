	function initialize() { 

				document.getElementById('contenido-mapa').innerHTML="<section id='map-canvas'></section>"

			var mapOptions = {center: new google.maps.LatLng(37.1773363, -3.5985571), zoom: 17, disableDefaultUI: true};
        		var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
			
			if(navigator.geolocation) {
				navigator.geolocation.getCurrentPosition(function(position) {
					var myLatlng = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
					var contentString = '<div id="content">'+
						'<div id="bodyContent">'+
			   			'<p>Te encuentras<br>aquí.</p>' +
						'</div>'+
						'</div>';
					
					var infowindow = new google.maps.InfoWindow({
						content: contentString
					});
					var marker = new google.maps.Marker({
						position: myLatlng,
						map: map,
						title: 'Localización'
					});

					google.maps.event.trigger(map, 'resize');
					  
					google.maps.event.addListener(marker, 'click', function() {
						infowindow.open(map,marker);
					});
				  	map.setCenter(myLatlng);
				}, function() {	handleNoGeolocation(true);
							  });
			} else {
				// Navegador no soporta geolocalización
				handleNoGeolocation(false);
			}
		}


	function handleNoGeolocation(errorFlag) {
		if (errorFlag) {
			var content = 'Error: El servicio de geolocalización no se encuentra disponible.';
		} else {
			var content = 'Error: Tu navegador no soporta geolocalización.';
		}
		var options = {
			map: map,
			position: new google.maps.LatLng(60, 105),
			content: content
		};
		var infowindow = new google.maps.InfoWindow(options);
		map.setCenter(options.position);
	}

	//google.maps.event.addDomListener(window, 'load', initialize);


	var map_simple;
	function initialize2() {

				document.getElementById('contenido-mapa').innerHTML="<section id='map-canvas'></section>"

	  var mapOptions = {
	    zoom: 8,
	    center: new google.maps.LatLng(	37.17734, -3.59856)
	  };
	  map_simple = new google.maps.Map(document.getElementById('map-canvas'),
	      mapOptions);
	}


	var geocoder;
	function initialize3() {

		document.getElementById('contenido-mapa').innerHTML= "<section id='panel'><input id='address' type='textbox' value='Sydney, NSW'><input type='button' value='Geocode' onclick='codeAddress()'></section><section id='map-canvas'></section>";

	  geocoder = new google.maps.Geocoder();
	  var latlng = new google.maps.LatLng(-34.397, 150.644);
	  var mapOptions = {
	    zoom: 8,
	    center: latlng
	  }
	  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

	}

	function codeAddress() {
	  var address = document.getElementById('address').value;
	  geocoder.geocode( { 'address': address}, function(results, status) {
	    if (status == google.maps.GeocoderStatus.OK) {
	      map.setCenter(results[0].geometry.location);
	      var marker = new google.maps.Marker({
	          map: map,
	          position: results[0].geometry.location
	      });
	    } else {
	      alert('Geocode was not successful for the following reason: ' + status);
	    }
	  });
	}


var elevator;
var infowindow = new google.maps.InfoWindow();
var denali = new google.maps.LatLng(63.3333333, -150.5);

function initialize4() {
					document.getElementById('contenido-mapa').innerHTML="<section id='map-canvas'></section>"

  var mapOptions = {
    zoom: 8,
    center: denali,
    mapTypeId: 'terrain'
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  // Create an ElevationService
  elevator = new google.maps.ElevationService();

  // Add a listener for the click event and call getElevation on that location
  google.maps.event.addListener(map, 'click', getElevation);
}

function getElevation(event) {

  var locations = [];

  // Retrieve the clicked location and push it on the array
  var clickedLocation = event.latLng;
  locations.push(clickedLocation);

  // Create a LocationElevationRequest object using the array's one value
  var positionalRequest = {
    'locations': locations
  }

  // Initiate the location request
  elevator.getElevationForLocations(positionalRequest, function(results, status) {
    if (status == google.maps.ElevationStatus.OK) {

      // Retrieve the first result
      if (results[0]) {

        // Open an info window indicating the elevation at the clicked position
        infowindow.setContent('The elevation at this point <br>is ' + results[0].elevation + ' meters.');
        infowindow.setPosition(clickedLocation);
        infowindow.open(map);
      } else {
        alert('No results found');
      }
    } else {
      alert('Elevation service failed due to: ' + status);
    }
  });
}


function initialize5() {

					document.getElementById('contenido-mapa').innerHTML="<section id='map-canvas'></section>"

  var myLatlng = new google.maps.LatLng(	37.17734, -3.59856);
  var mapOptions = {
    zoom: 13,
    center: myLatlng
  }

  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var trafficLayer = new google.maps.TrafficLayer();
  trafficLayer.setMap(map);
}


var directionsDisplay;
var directionsService = new google.maps.DirectionsService();

function initialize6() {

	document.getElementById('contenido-mapa').innerHTML= "<section id='panel'><b><font color='black'>Origen: </font></b><input id='start' type='textbox' value='Granada'><b><font color='black'> Destino: </font></b><input id='end' type='textbox' value='Malaga'><input type='button' value='Calcular ruta' onclick='calcRoute()'></section><section id='map-canvas'></section>";

  directionsDisplay = new google.maps.DirectionsRenderer();
  var chicago = new google.maps.LatLng(41.850033, -87.6500523);
  var mapOptions = {
    zoom:7,
    center: chicago
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  directionsDisplay.setMap(map);
}

function calcRoute() {
  var start = document.getElementById('start').value;
  var end = document.getElementById('end').value;
  var request = {
      origin:start,
      destination:end,
      travelMode: google.maps.TravelMode.DRIVING
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    }
  });
}


function initialize8() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };
                    
    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);
        
    // Multiple Markers
    var markers = [
        ['London Eye, London', 51.503454,-0.119562],
        ['Palace of Westminster, London', 51.499633,-0.124755]
    ];
                        
    // Info Window Content
    var infoWindowContent = [
 
    ];
        
    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    
    // Loop through our array of markers & place each one on the map  
    for( i = 0; i < markers.length; i++ ) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            title: markers[i][0]
        });
        
        // Allow each marker to have an info window    
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }

    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(14);
        google.maps.event.removeListener(boundsListener);
    });
    
}