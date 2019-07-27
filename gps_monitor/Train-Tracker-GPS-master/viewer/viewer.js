$(document).ready(function () {

    var updateInterval = 5*1000,
        replaySpeed = 100,
        tailLength = (60/(updateInterval/1000)),
        map,
        runnerCount = 0,
        runners = [],
        socketServer = 'http://localhost:8080';

    function runner(json,id) {
		console.log("runner");
        var data = [],
            path = new google.maps.MVCArray(),
            poly,
            polySymbol,
            colors = ["#FF0000", "#FF69B4", "#00FF7F", "#FF00FF", "#FFA500", "#00FF00",
                      "#FA8072", "#00FFFF", "#ADFF2F", "#00FF7F"],
            runnerColor = colors[Math.floor(Math.random()*colors.length)],
            popInterval,
            isPlaying = false,
            lastUpdate = Date.now(),
            lastPoint,
            r = {};

        r.id = json.runners[id].runnerid;

        $('[data-id="'+id+'"] .runnercolor').val(runnerColor);

        if(!data.length){ populate(); }

        function populate(){
			console.log("populate");
            var lats = json.runners[id].lat.split(",");
            var lons = json.runners[id].lon.split(",");
            var speeds = json.runners[id].speed.split(",");

            for (var i = lons.length - 1; i >= 0; i--) {
                var p = new google.maps.LatLng(lats[i], lons[i]);
                p.speed = speeds[i];
                data.push(p);
            }
            map.setCenter(data[data.length-1]);
            makePath(tailLength*2,true);
        }

        function makePath(length,poly){
			
			console.log('path before clear ',path);
            path.clear();
            console.log('makin path, length: '+length);
			console.log('data ',data);
            // prevents trying to access out of range points
            if(data.length < length){
                length = data.length-1;
            }

            for (var i=0; i<length; i++){
                if(length-i < length-1){
                    path.push(interpolate(data[data.length-length+i],data[data.length-length+i-1]));
                }
                path.push(data[data.length-length+i]);
            }
			console.log('path after clear',path);
            if(poly){
                makePoly();
            }
        }

        function makePoly(){
            polySymbol = {
                path: google.maps.SymbolPath.CIRCLE,
                strokeColor: "black",
                fillColor: runnerColor,
                fillOpacity: 1,
                strokeWeight: 2,
                scale: 6
            };
			console.log("makePoly path", path);
            poly = new google.maps.Polyline({
                path: path,
                strokeColor: runnerColor,
                strokeOpacity: 1,
                strokeWeight: 5,
                clickable: false,
                map: map,
                icons: [{icon: polySymbol, offset: '100%'}]
            });
        }

        function displayPace(pace) {
            $('[data-id="'+id+'"] .pace').html(getPace(pace));
        }

        function pop() {
			// tungnt
            if(path.getLength() > 2){
                path.removeAt(0);
            }
        }

        function conditionalPop() {
            // this is exectued every 2.5 sek. It looks at the time elapsed between now and the last data reciept.
            // If that time is higher than the updateInterval, the runner has stopped sending or hasn't moved,
            // see r.update. OR, if the tail length is longer than allowed, it's popped.

            var now = Date.now();
            var diff = now-lastUpdate;
			console.log("diff ", diff);
			console.log("now-lastUpdate ", now-lastUpdate);
            if (diff > updateInterval || path.getLength() > tailLength*2){
                if(!isPlaying){
                    pop();
                }
            }
            else{
                console.log('nopop');
            }
        }

        popInterval = setInterval(conditionalPop, (updateInterval/2));

        r.pop = function() {
            pop();
        };

        r.update = function(json) {
			console.log("update current runner");
            var newLat = json.lat;
            var newLon = json.lon;
            var newSpeed = json.speed;
            var p = new google.maps.LatLng(newLat, newLon);

            if(lastPoint !== p.toString()) {
                // movement found, add new point to data[] and MVCArray
                displayPace(newSpeed);
                p.speed = newSpeed;
                data.push(p);
				console.log("data after pushing ", data);
                if(!isPlaying) {
                    path.push(interpolate(p, data[data.length-2 ]));
                    setTimeout(function() {
                        if(!isPlaying){
                            path.push(p);
                        }
                    }, (updateInterval)/2);
                }
                lastUpdate = Date.now();
                console.log("movement detected");
            }else{
                console.log('no movement');
				console.log("data after pushing ", data);
                data.push(p);
            }
            lastPoint = p.toString();
        };

        r.replay = function() {
			console.log("replay data=",data);
            if(!isPlaying) {
                var currLen = parseInt((path.getLength()/2)+1);
                path.clear();
                path.push(data[0]);
                path.push(interpolate(data[1], data[0]));
                var i = 1;
                isPlaying = true;
                replayPoint();
            }
            
            function replayPoint() {
				//console.log("replayPoint");
                if(i === data.length-1) {
					// tungnt
                    path.push(data[i]);
                    displayPace(data[i].speed);
                    console.log('breaking');
                    makePath(currLen,false);
                    isPlaying = false;
                }
                else {
                    path.push(data[i]);
                    setTimeout(function() { path.push(interpolate(data[i], data[i-1])); }, replaySpeed/2);
                    displayPace(data[i].speed);
                    i++;
					// tungnt
                    setTimeout(function() { requestAnimationFrame(replayPoint); }, replaySpeed);
                }
            }
        };

        r.setColor = function(color){
            poly.setOptions({strokeColor:color});
            polySymbol.fillColor = color;
            runnerColor = color;
        };
        
		// tungnt
		r.setVisible = function(value) {
			if(poly){
				poly.setVisible(value);
			}
		}
		
        return r;
    }

    function makeRunners(json){
        console.log('makerunners json',json);
        if(json.runners.length === 0){
            //alert('No runners recieved');
           // toggleTimer();
        }

        for (var i=0; i<json.runners.length; i++) {
            lastspeed = json.runners[i].speed.split(",");
            $('#runnerlist').append('<tr data-id='+i+'><td><input title="Change color" type="color" class="runnercolor" value="#FFFFF"/><span title="Replay" class="replay">↻</span>'+json.runners[i].runnerid+'</td><td class="pace">'+getPace(lastspeed[0])+'</td><td><input type="checkbox" checked data-vehicle-id="'+json.runners[i].runnerid+'" class="show_vehicle" name="show_vehicle"></td></tr>');
            runners.push(runner(json,i));
            runnerCount = i;
        }
		console.log('makerunners runners',runners);
    }

    function updateRunners(data){
        function currentRunner(data){
            for (var i = runners.length - 1; i >= 0; i--) {
                if(runners[i].id === data.id) {
                    return i;
                }
            }
        }

        runners[currentRunner(data)].update(data);
		console.log('updateRunners runners',runners);

    }

    function setSpeed(speed){
        replaySpeed = speed;
        $("[for=replayspeed]").html('Replay time: '+replaySpeed);
    }

    function interpolate(fresh,old) {
        var intLat = (old.lat()+fresh.lat())/2;
        var intLon = (old.lng()+fresh.lng())/2;
        return new google.maps.LatLng(intLat, intLon);
    }

    function getPace(pace) {
        if (pace === 0 || isNaN(pace)) {
            return "N/A";
        } 
        else {
            var onemin = pace * 60;
            var x = 1000 / onemin;
            var time = 60 * x;
            var minutes = Math.floor(time / 60);
            var seconds = ((Math.round(time - minutes * 60)).toString());
            if (seconds.length === 1) { seconds = "0" + seconds; }
            return minutes + ":" + seconds;
        }
    }

    // Socket.io stuff

    var socket = io.connect(socketServer);

    socket.emit('client');

    socket.on('sendfromserver', function (data) {
		console.log('data sendfromserver ',data);
        updateRunners(data);
    });

    socket.on('allData', function (json) {
        makeRunners(JSON.parse(json));
    });

    // Map stuff
    var mapOptions = {
        center: new google.maps.LatLng(63.845224,20.073608),
        zoom: 14,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        streetViewControl: false,
        panControl: false
    };
    
    var osm = new google.maps.ImageMapType({
        getTileUrl: function(coord, zoom) {
            return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
        },
        tileSize: new google.maps.Size(256, 256),
        isPng: true,
        maxZoom: 18,
        name: "OSM",
        alt: "OpenStreetMap"
    });

    var OLmaps = new google.maps.ImageMapType({
        getTileUrl: function(coord, zoom) {
            return "http://YOUR CUSTOM TILE SERVER URL" + zoom + "/" + coord.x + "/" + coord.y + ".png";
        },
        tileSize: new google.maps.Size(256, 256),
        isPng: true,
        maxZoom: 16,
        name: "OL maps",
        alt: "OL maps"
    });

    function toggleMap() {
        if(map.overlayMapTypes.getAt(0)){
            map.overlayMapTypes.removeAt(0);
        }
        else{
            map.overlayMapTypes.insertAt(0, OLmaps);
        }
    }

    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);

    map.mapTypes.set('osm', osm);
    map.setOptions({
    mapTypeControlOptions: {
        mapTypeIds:
            ['osm',
            google.maps.MapTypeId.ROADMAP,
            // google.maps.MapTypeId.TERRAIN,
            google.maps.MapTypeId.SATELLITE],
            // google.maps.MapTypeId.HYBRID],
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR
        }
    });

    // Event handlers
    $("[for=replayspeed]").text('Replay time: '+replaySpeed);
    $('#replayspeed').on('change', function(){ setSpeed($(this).val()); });
    $('#togglemap').on('change', toggleMap);
    $('#runnerlist').on('change', '.runnercolor', function(event){
        var id = $(this).closest('tr').attr('data-id');
        var newColor = $('[data-id="'+id+'"] .runnercolor').val();
        runners[id].setColor(newColor);
    });
    $('#runnerlist').on('click', '.replay', function(event){
        var id = $(this).closest('tr').attr('data-id');
        runners[id].replay();
    });
	$('#settings').on('change', '.show_vehicle', function(){
		function currentRunner(vehicle_id){
            for (var i = runners.length - 1; i >= 0; i--) {
                if(runners[i].id === vehicle_id) {
                    return i;
                }
            }
        }
		
		var vehicle_id = $(this).data('vehicle-id');
		console.log(runners[currentRunner(vehicle_id)]);
		runners[currentRunner(vehicle_id)].setVisible(this.checked);
		
	});
    // http://paulirish.com/2011/requestanimationframe-for-smart-animating/
    // http://my.opera.com/emoller/blog/2011/12/20/requestanimationframe-for-smart-er-animating
    // requestAnimationFrame polyfill by Erik Möller
    // fixes from Paul Irish and Tino Zijdel
    (function() {
        var lastTime = 0;
        var vendors = ['ms', 'moz', 'webkit', 'o'];
        for(var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
            window.requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
            window.cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame'] 
                                       || window[vendors[x]+'CancelRequestAnimationFrame'];
        }
     
        if (!window.requestAnimationFrame)
            window.requestAnimationFrame = function(callback, element) {
                var currTime = new Date().getTime();
                var timeToCall = Math.max(0, 16 - (currTime - lastTime));
                var id = window.setTimeout(function() { callback(currTime + timeToCall); }, 
                  timeToCall);
                lastTime = currTime + timeToCall;
                return id;
            };
     
        if (!window.cancelAnimationFrame)
            window.cancelAnimationFrame = function(id) {
                clearTimeout(id);
            };
    }());
});