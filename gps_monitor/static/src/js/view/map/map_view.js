odoo.define('gps_monitor.MapView', function (require) {
    'use strict';

    var BasicView = require('web.BasicView');
    var core = require('web.core');
    var MapModel = require('gps_monitor.MapModel');
    var MapRenderer = require('gps_monitor.MapRenderer');
    var MapController = require('gps_monitor.MapController');
    var _lt = core._lt;

    var MapView = BasicView.extend({
        accesskey: 'm',
        display_name: _lt('Map'),
        icon: 'fa-map-o',
        jsLibs: [],
        config: _.extend({}, BasicView.prototype.config, {
            Model: MapModel,
            Renderer: MapRenderer,
            Controller: MapController
        }),
        viewType: 'gmap',
        init: function (viewInfo, params) {
            console.log('init');
            this._super.apply(this, arguments);
            var arch = viewInfo.arch;
            var attrs = arch.attrs;
            this.rendererParams.arch = arch;
            this.rendererParams.show_log_data = attrs.show_log_data;
            this.rendererParams.show_filter_time = attrs.show_filter_time;
            this.rendererParams.is_monitor = attrs.is_monitor;
        },
    });

    return MapView;

});