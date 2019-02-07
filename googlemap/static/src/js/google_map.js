odoo.define('googlemap.FieldGoogleMap', function(require) {
    "use strict";
    var field_registry = require('web.field_registry');
    var AbstractField = require('web.AbstractField');
    var FieldGoogleMap = AbstractField.extend({
    template: 'FieldGoogleMap',
    start: function() {
        console.log("FieldGoogleMap start ");
        var self = this;
        self.init_map();
        return this._super();
    },

    init_map: function () {
        console.log("init_map start ");
        console.log(this.el);
        var self = this;
        console.log($(this.el).find('#tung_google_map_search')[0]);
        var searchBox = new google.maps.places.SearchBox($(this.el).find('#tung_google_map_search')[0]);
        var markers = [];
        searchBox.addListener('places_changed', function() {
            var places = searchBox.getPlaces();

              if (places.length == 0) {
                 return;
              }

              // Clear out the old markers.
              markers.forEach(function(marker) {
                marker.setMap(null);
              });
              markers = [];

              // For each place, get the icon, name and location.
              var bounds = new google.maps.LatLngBounds();
              places.forEach(function(place) {
                if (!place.geometry) {
                  console.log("Returned place contains no geometry");
                  return;
                }
                var icon = {
                  url: place.icon,
                  size: new google.maps.Size(71, 71),
                  origin: new google.maps.Point(0, 0),
                  anchor: new google.maps.Point(17, 34),
                  scaledSize: new google.maps.Size(25, 25)
                };

                // Create a marker for each place.
                markers.push(new google.maps.Marker({
                  map: self.map,
                  icon: icon,
                  title: place.name,
                  position: place.geometry.location
                }));

                if (place.geometry.viewport) {
                  // Only geocodes have viewport.
                  bounds.union(place.geometry.viewport);
                } else {
                  bounds.extend(place.geometry.location);
                }
              });
              self.map.fitBounds(bounds);
        });

        this.map = new google.maps.Map($(this.el).find('#tung_googlemap')[0], {
            center: {lat:0,lng:0},
            zoom: 2,
            disableDefaultUI: true,
        });
        this.marker = new google.maps.Marker({
            position: {lat:0,lng:0},
        });

        if(this.value) {
            this.marker.setPosition(JSON.parse(this.value).position);
            this.map.setCenter(JSON.parse(this.value).position);
            this.map.setZoom(JSON.parse(this.value).zoom);
            this.marker.setMap(this.map);
        }

        this.map.addListener('click', function(e) {
            console.log('map click');
            console.log('mode ', self.mode);
            if(self.mode === 'edit' && self.marker.getMap() == null) {
                self.marker.setPosition(e.latLng);
                self.marker.setMap(self.map);
                self._setValue(JSON.stringify({position:self.marker.getPosition(),zoom:self.map.getZoom()}));
            }
        });
        this.map.addListener('zoom_changed', function() {
            console.log('map zoom_changed');
            if(self.mode === 'edit' && self.marker.getMap()) {
                self._setValue(JSON.stringify({position:self.marker.getPosition(),zoom:self.map.getZoom()}));
            }
        });
        this.marker.addListener('click', function() {
            console.log('marker click');
            if(self.mode === 'edit') {
                self.marker.setMap(null);
                self._setValue(false);
            }
        });
        this.marker.addListener('dragend', function() {
            console.log('marker dragend');
            self._setValue(JSON.stringify({position:self.marker.getPosition(),zoom:self.map.getZoom()}));
        });
    }
});

field_registry.add('googlemap', FieldGoogleMap);

return {
    FieldGoogleMap: FieldGoogleMap,
};
});
