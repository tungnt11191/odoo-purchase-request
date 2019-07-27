odoo.define('gps_monitor.view_registry', function (require) {
    "use strict";

    var MapView = require('gps_monitor.MapView');
    var view_registry = require('web.view_registry');

    view_registry.add('gmap', MapView);

});
