odoo.define('gps_monitor.MapRenderer', function (require) {
    'use strict';

    var BasicRenderer = require('web.BasicRenderer');
    var core = require('web.core');
    var QWeb = require('web.QWeb');
    var session = require('web.session');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var KanbanRecord = require('web.KanbanRecord');

    var qweb = core.qweb;

    var updateInterval = 5*1000,
        replaySpeed = 100,
        tailLength = (60/(updateInterval/1000)),
        map,
        runnerCount = 0,
        runners = [],
        socketServer = socket_io_server;

    var MapRenderer = BasicRenderer.extend({
        className: 'o_map_view',
        template: 'gps_monitor.MapView',
        /**
         * @override
         */
        init: function (parent, state, params) {
            console.log("gps monitor init");
            this.socket = io.connect(this.socketServer);
            this.is_search_time = params.show_filter_time;
            this.show_log_data = params.show_log_data;
            this.is_monitor = params.is_monitor;
            this._super.apply(this, arguments);
        },

        /**
         * @override
         */
        start: function () {
            console.log("gps monitor start");
            var self = this;

            if(self.is_search_time == 'false') {
                this.$('.search_box').addClass('hide');
            }

            if(self.show_log_data == 'false') {
                this.$('.table-vehicle-data').addClass('hide');
            }

            this.socket.emit('client');

            if(self.is_monitor == 'true') {
                this.socket.on('sendfromserver', function (data) {
                    console.log('data sendfromserver ',data);
                    self.updateRunners(data);
                });
            }
            if(self.is_monitor == 'false') {
                 this.socket.on('senddatatoclient', function (data) {
                    console.log('data senddatatoclient ',data);

                    self.replaceRunners(JSON.parse(data));
                });
            }

            this.socket.on('allData', function (json) {
                self.makeRunners(JSON.parse(json));
                // for demo data
                if(self.is_monitor == 'true'){
                    self.runners[0].replay();
                }
            });

            ///////////////////////
            this.$('.o_map_view').empty();
            this.map = new google.maps.Map(this.$('.o_map_view').get(0), this.mapOptions);
            this.map.mapTypes.set('osm', this.osm);
            this.map.setOptions({
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
            this.$("[for=replayspeed]").text('Replay time: '+this.replaySpeed);
            this.$('#replayspeed').on('change', function(){ self.setSpeed($(this).val()); });
            this.$('#togglemap').on('change', this.toggleMap(this.map));
            this.$('#runnerlist').on('change', '.runnercolor', function(event){
                var id = $(this).closest('tr').attr('data-id');
                var newColor = $('[data-id="'+id+'"] .runnercolor').val();
                self.runners[id].setColor(newColor);
            });
            this.$('#runnerlist').on('click', '.replay', function(event){
                var id = $(this).closest('tr').attr('data-id');
                self.runners[id].replay();
            });
            this.$('#runnerlist').on('change', '.show_vehicle', function(){
                var vehicle_id = $(this).data('vehicle-id');
                var currentRunnerIndex = self.getCurrentRunnerIndex(vehicle_id);
                runners[currentRunnerIndex].setVisible(this.checked);
                runners[currentRunnerIndex].replay();
                self.showTrackingData(vehicle_id);

            });

            this.$('#search_vehicle_id').on('change', function(){

            });

            this.$('#search_vehicle_id').keypress(function(event){
                var keycode = (event.keyCode ? event.keyCode : event.which);
                if(keycode == '13'){
                    var search_vehicle_id_value = $(this).val();
                    var searchRunnerIndex = self.getCurrentRunnerIndex(search_vehicle_id_value);
                    if (searchRunnerIndex>=0){
                        self.map.setCenter(runners[searchRunnerIndex].getLastPosition());
                    }
                }
                //Stop the event from propogation to other handlers
                //If this line will be removed, then keypress event handler attached
                //at document level will also be triggered
                event.stopPropagation();
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

            this.$('input[name="datetimes"]').daterangepicker({
                timePicker: false,
                startDate: self.filter_startDate,
                endDate: self.filter_endDate,
                locale: {
                  format: 'DD/MM/YYYY HH:mm:ss'
                }
            });
            this.$('input[name="datetimes"]').on('apply.daterangepicker', function(ev, picker) {
                console.log(picker.startDate.format('YYYY-MM-DD'));
                console.log(picker.endDate.format('YYYY-MM-DD'));
                self.filter_startDate = picker.startDate;
                self.filter_endDate = picker.endDate;
            });

            this.$(".ft_theme_switcher").on('click', '.toggle', function(){
                var b=$(this).parent();
                if(b.hasClass("ocult")){
                    var c={right:"0"};
                    b.animate(c,500);
                }
                else{
                    var d={right:"-400px"};
                    b.animate(d,500);
                }
                b.toggleClass("ocult")}
            );

            self.runnerListTable = this.$('#runnerlist').DataTable( {
                columnDefs: [
//                  {
//                    targets: 0,
//                    createdCell: function (cell, cellData, rowData, rowIndex, colIndex) {
//                      $(cell).css('color', 'green');   //add style to cell
//                    }
//                  },
//                  {
//                    targets: 1,
//                    render: function (data, type, row, meta) {
//                      return '<a href="https://datatables.net">datatables</a>';  //render link in cell
//                    }
//                  },
                      {
                        targets: 2,
                        render: function (data, type, row, meta) {
                          return '<input title="Change color" type="color" class="runnercolor" value="#FFFFF"/>';  //render link in cell
                        }
                      },
                      {
                        targets: 4,
                        render: function (data, type, row, meta) {
                          return '<!--<span title="Replay" class="replay">↻</span> --> <input type="checkbox" data-vehicle-id="'+data+'" class="show_vehicle" name="show_vehicle">';  //render link in cell
                        }
                      }
                ],

                createdRow: function (row, data, index) {
                   //self.$(row).data('id',index);   //add class to row
                   //$(row).addClass('blue');
                   $(row).attr('data-id', index);
                   //$('td', row).eq(2).css('font-weight', 'bold');
                }
            } );
            this.$('#runnerlist').on('click', 'tr', function(){
                var vehicle_index_id = $(this).data('id');
                var search_runner = self.runners[vehicle_index_id];
                self.map.setCenter(search_runner.getLastPosition());
                if(self.is_monitor == 'false'){
                    var outObj = {
                        startDate:  self.filter_startDate,
                        endDate:    self.filter_endDate,
                        vehicle_id: search_runner.id
                    };

                    var out = JSON.stringify(outObj);
                    self.socket.emit('sendrequesttoserver', out);
                }

            });
            return this._super();
        },

        is_search_time: false,
        updateInterval : updateInterval,
        replaySpeed : replaySpeed,
        tailLength : tailLength,
        map : map,
        runnerCount : runnerCount,
        runners : runners,
        socketServer : socketServer,
        runnerListTable : null,

        filter_startDate: moment().startOf('hour'),
        filter_endDate: moment().startOf('hour').add(24, 'hour'),
        runner : function(json,id) {
            console.log("runner");
            var self = this;

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
                lastPosition,
                infowindow = new google.maps.InfoWindow(),
                r = {};
            r.is_visible = false;
            r.id = json.runners[id].runnerid;

            $('[data-id="'+id+'"] .runnercolor').val(runnerColor);

            if(!data.length){ populate(); }

            function populate(){
                console.log("populate");
                var lats = json.runners[id].lat.split(",");
                var lons = json.runners[id].lon.split(",");
                var speeds = json.runners[id].speed.split(",");
                var times = json.runners[id].time.split(",");

                for (var i = lons.length - 1; i >= 0; i--) {
                    var p = new google.maps.LatLng(lats[i], lons[i]);
                    p.speed = speeds[i];
                    p.time = times[i];
                    data.push(p);
                }
                self.map.setCenter(data[data.length-1]);
                makePath(self.tailLength*2,true);
            }

            function makePath(length,poly){
                path.clear();
                console.log('makin path, length: '+length);
                console.log('data ',data);
                // prevents trying to access out of range points
                if(data.length < length){
                    length = data.length-1;
                }

                if(self.is_monitor == 'false'){
                    for (var i=0; i<length; i++){
                        if(length-i < length-1){
                            path.push(self.interpolate(data[data.length-length+i],data[data.length-length+i-1]));
                        }
                        path.push(data[data.length-length+i]);
                    }
                } else if(self.is_monitor == 'true') {
                    path.push(data[data.length-2]);
                    path.push(data[data.length-1]);
                }

                console.log('path ',path);
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
                console.log("makePoly");
                poly = new google.maps.Polyline({
                    path: path,
                    strokeColor: runnerColor,
                    strokeOpacity: 1,
                    strokeWeight: 5,
                    clickable: true,
                    map: self.map,
                    icons: [{icon: polySymbol, offset: '100%'}],
                });
                poly.vehicle = $.extend({}, json.runners[id]);
                createInfoWindow(poly);
            }
            function createInfoWindow(poly) {
                google.maps.event.addListener(poly, 'click', function(event) {
                    // infowindow.content = content;
                    infowindow.setContent(this.vehicle.runnerid);

                    // infowindow.position = event.latLng;
                    infowindow.setPosition(event.latLng);
                    infowindow.open(self.map);


//                    var latlng=event.latLng;
//                     console.log(poly);
//                     var needle = {
//                         minDistance: 9999999999, //silly high
//                         index: -1,
//                         latlng: null
//                     };
//                     poly.getPath().forEach(function(routePoint, index){
//                         var dist = google.maps.geometry.spherical.computeDistanceBetween(latlng, routePoint);
//                         if (dist < needle.minDistance){
//                            needle.minDistance = dist;
//                            needle.index = index;
//                            needle.latlng = routePoint;
//                         }
//                     });
                     // The closest point in the polyline
                     //console.log("Closest index: " + needle.index);

                     // The clicked point on the polyline
                     //console.log(latlng);
                });
            }
            function displayPace(pace) {
                $('[data-id="'+id+'"] .pace').html(self.getPace(pace));
            }

            function pop() {
//            tungnt
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
                if (diff > self.updateInterval || path.getLength() > self.tailLength*2){
                    if(!isPlaying){
//                    tungnt
                        if (r.is_visible == false){
                            pop();
                        }
                    }
                }
                else{
                    console.log('nopop');
                }
            }

            popInterval = setInterval(conditionalPop, (self.updateInterval/2));

            r.pop = function() {
                pop();
            };

            r.update = function(json) {
                console.log("update current runner");
                var newLat = json.lat;
                var newLon = json.lon;
                var newSpeed = json.speed;
                var newTime = json.time;
                var p = new google.maps.LatLng(newLat, newLon);

                if(lastPoint !== p.toString()) {
                    // movement found, add new point to data[] and MVCArray
                    displayPace(newSpeed);
                    p.speed = newSpeed;
                    p.time = newTime;
                    data.push(p);
                    console.log("data after pushing ", data);
                    if(!isPlaying) {
                        path.push(self.interpolate(p, data[data.length-2 ]));
                        setTimeout(function() {
                            if(!isPlaying){
                                path.push(p);
                            }
                        }, (self.updateInterval)/2);
                    }
                    lastUpdate = Date.now();
                    console.log("movement detected");
                }else{
                    console.log('no movement');
                    console.log("data after pushing ", data);
                    data.push(p);
                }
                lastPoint = p.toString();
                lastPosition = p;
            };

            r.replay = function() {
                console.log("replay data=",data);
                if(!isPlaying) {
                    //var currLen = parseInt((path.getLength()/2)+1);
                    var currLen = parseInt(path.getLength());
                    path.clear();
                    path.push(data[0]);
                    path.push(self.interpolate(data[1], data[0]));
                    var i = 1;
                    isPlaying = true;
                    replayPoint();
                }

                function replayPoint() {
                    //console.log("replayPoint");
                    if(i === data.length-1) {
                        path.push(data[i]);
                        displayPace(data[i].speed);
                        console.log('breaking');
                        makePath(currLen,false);
                        isPlaying = false;
                    }
                    else {
                        path.push(data[i]);
                        setTimeout(function() { path.push(self.interpolate(data[i], data[i-1])); }, self.replaySpeed/2);
                        displayPace(data[i].speed);
                        i++;
                        setTimeout(function() { requestAnimationFrame(replayPoint); }, self.replaySpeed);
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
                    this.is_visible = value;
                    poly.setVisible(value);
                }
            };
            r.clearPath = function() {
                if(poly){
                    poly.setMap(null);
                }
            };
            r.getPath= function(){
                return path;
            };

            r.getData= function(){
                return data;
            };

            r.getPoly= function(){
                return poly;
            };
            r.getLastPosition = function(){
                var allPath = this.getPath().getArray();
                var lastPath = allPath[allPath.length-1];
                return new google.maps.LatLng(lastPath.lat(), lastPath.lng());
            };
            return r;
        },
        showTrackingData:function(vehicle_id){
            var self = this;
            var currentRunnerIndex = self.getCurrentRunnerIndex(vehicle_id);
            var currentRunner = self.runners[currentRunnerIndex];
            if (currentRunnerIndex != undefined || currentRunnerIndex>-1){
                if(currentRunner.is_visible){
                    var currentRunnerPath = currentRunner.getPath().getArray();

                    for(var j =0 ; j< currentRunnerPath.length ; j++){
                        if(currentRunnerPath[j].speed != undefined){
                            var data_row = '<tr>'
                                         +      '<td>'+currentRunnerPath[j].lng()+'</td>'
                                         +      '<td>'+currentRunnerPath[j].lat()+'</td>'
                                         +      '<td>'+currentRunnerPath[j].speed+'</th>'
                                         +      '<td>'+(new Date(currentRunnerPath[j].time)).toLocaleString()+'</td>'
                                         + '</tr>'
                            $('#vehicle_tracking_data tbody').prepend(data_row);

                        }

                    }
                } else {
                    $('#vehicle_tracking_data tbody').empty()
                };


            }
        },
        makeRunners : function(json){
            var self = this;
            console.log('makerunners json',json);
            if(json.runners.length === 0){
                //alert('No runners recieved');
               // toggleTimer();
            }

            for (var i=0; i<json.runners.length; i++) {
                var lastspeed = json.runners[i].speed.split(",");
                var lasttime = json.runners[i].time.split(",");

                var vehicle_row = '<tr data-id='+i+'>'
                                +   '<td>'+json.runners[i].runnerid+'</td>'
                                +   '<td>'+this.getPace(lastspeed[0])+'</td>'
                                +   '<td><input title="Change color" type="color" class="runnercolor" value="#FFFFF"/></td>'
                                +   '<td>01-01 12:00</td>'
                                +   '<td><span title="Replay" class="replay">↻</span><input type="checkbox" data-vehicle-id="'+json.runners[i].runnerid+'" class="show_vehicle" name="show_vehicle"></td>'
                                +   '</tr>';

                //$('#runnerlist').append('<tr data-id='+i+'><td><input title="Change color" type="color" class="runnercolor" value="#FFFFF"/><span title="Replay" class="replay">↻</span>'+json.runners[i].runnerid+'</td><td class="pace">'+this.getPace(lastspeed[0])+'</td><td><input type="checkbox" checked data-vehicle-id="'+json.runners[i].runnerid+'" class="show_vehicle" name="show_vehicle"></td></tr>');
                //$('#runnerlist').append(vehicle_row);
                self.runnerListTable.row.add([json.runners[i].runnerid,this.getPace(lastspeed[0]),'1',(new Date(lasttime[0])).toLocaleString(),json.runners[i].runnerid ]).draw();
                self.runners.push(self.runner(json,i));
                self.runnerCount = i;
            }
            console.log('makerunners runners',self.runners);
        },

        replaceRunners : function(json){
            var self = this;
            console.log('replaceRunners json',json);

            for (var i=0; i<json.runners.length; i++) {
                var lastspeed = json.runners[i].speed.split(",");
                var lasttime = json.runners[i].time.split(",");

                var updated_vehicle_id = json.runners[i].runnerid;
                var updated_vehicle_index = self.getCurrentRunnerIndex(updated_vehicle_id)
                self.runners[updated_vehicle_index].clearPath()
                self.runners[updated_vehicle_index] = self.runner(json,0);
                self.runnerCount = i;
            }
        },


        getCurrentRunnerIndex: function(vehicle_id){
            var self = this;
            for (var i = self.runners.length - 1; i >= 0; i--) {
                if(self.runners[i].id === vehicle_id) {
                    return i;
                }
            }
            return -1;
        },
        updateRunners : function(data){
            var self = this;
            //tungnt
            var currentRunnerIndex = self.getCurrentRunnerIndex(data.id);
            if (currentRunnerIndex != undefined && currentRunnerIndex>-1 && self.runners[currentRunnerIndex] != undefined){
                self.runners[currentRunnerIndex].update(data);
            }
        },

        setSpeed : function(speed){
            this.replaySpeed = speed;
            $("[for=replayspeed]").html('Replay time: '+this.replaySpeed);
        },

        interpolate : function(fresh,old) {
            var intLat = (old.lat()+fresh.lat())/2;
            var intLon = (old.lng()+fresh.lng())/2;
            return new google.maps.LatLng(intLat, intLon);
        },

        getPace : function(pace) {
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
        },

        // Socket.io stuff
        socket : null,
        // Map stuff
        mapOptions : {
            center: new google.maps.LatLng(63.845224,20.073608),
            zoom: 14,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            streetViewControl: false,
            panControl: false
        },

        osm : new google.maps.ImageMapType({
            getTileUrl: function(coord, zoom) {
                return "http://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
            },
            tileSize: new google.maps.Size(256, 256),
            isPng: true,
            maxZoom: 18,
            name: "OSM",
            alt: "OpenStreetMap"
        }),

        OLmaps : new google.maps.ImageMapType({
            getTileUrl: function(coord, zoom) {
                return "http://YOUR CUSTOM TILE SERVER URL" + zoom + "/" + coord.x + "/" + coord.y + ".png";
            },
            tileSize: new google.maps.Size(256, 256),
            isPng: true,
            maxZoom: 16,
            name: "OL maps",
            alt: "OL maps"
        }),

        toggleMap : function(map) {
            if(map.overlayMapTypes.getAt(0)){
                map.overlayMapTypes.removeAt(0);
            }
            else{
                map.overlayMapTypes.insertAt(0, this.OLmaps);
            }
        },
    });

    return MapRenderer;

});