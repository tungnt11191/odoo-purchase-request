$(document).ready(function() {
    var socket = io.connect('http://localhost:8080');

    var latlon = {};
    while (!latlon.id) {
        latlon.id = prompt("Please enter your ID:", "");
    }
    var first = true;
    var intervalId;
    var watchId;

    socket.emit('runnerConnect', latlon.id+" connected as runner");

    function startTrack() {
        if(navigator.geolocation) {
            console.log('trying to find a fix');
            watchId = navigator.geolocation.watchPosition(geo_success, errorHandler,
            {enableHighAccuracy:true, maximumAge:30000, timeout:27000});
        }
        else{
            alert("Sorry, device does not support geolocation! Update your browser.");
        }
    }

    function geo_success(position) {
        $("#status p").text("Tracking active");
        $('#status').removeClass("stopped").addClass("active");
        $('button').text("Stop tracking");

        latlon.lat = position.coords.latitude;
        latlon.lon = position.coords.longitude;
        if(!position.coords.speed) { latlon.speed = 0; }
        else{ latlon.speed = position.coords.speed }
        
        if(first) {
            intervalId = setInterval(send, 15000);
        }
        first = false;
    }

    function addTime() {
        // insert time in formData-object
        var d = new Date();
        var d_utc = ISODateString(d);
        latlon.time = d_utc;

        // date to ISO 8601,
        // developer.mozilla.org/en/JavaScript/Reference/Global_Objects/Date#Example.3a_ISO_8601_formatted_dates
        function ISODateString(d) {
            function pad(n) {return n<10 ? '0'+n : n}
            return d.getUTCFullYear()+'-'
            + pad(d.getUTCMonth()+1)+'-'
            + pad(d.getUTCDate())+'T'
            + pad(d.getUTCHours())+':'
            + pad(d.getUTCMinutes())+':'
            + pad(d.getUTCSeconds())+'Z'
        }
    }

    function send() {
        addTime();
        socket.emit('sendevent', latlon);
    }

    function toggleTimer() {
        if(intervalId) {
            console.log('stopping');
            clearInterval(intervalId);
            intervalId = null;
            navigator.geolocation.clearWatch(watchId);
            $("#status p").text("Not tracking");
            $('#status').removeClass("active").addClass("stopped");
            $('button').text("Start tracking");
            first = true;
        }
        else{
            console.log('starting');
            startTrack();
        }
    }

    function errorHandler(err) { 
        if(err.code == 1) {
            alert("Error: Access was denied ",err);
        }
        else if(err.code == 2) {
            alert("Error: Position is unavailable");
        }
    }

    $('#startstop').on("click", toggleTimer);
});