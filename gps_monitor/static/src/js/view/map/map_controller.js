odoo.define('gps_monitor.MapController', function (require) {
    'use strict';

    var Context = require('web.Context');
    var core = require('web.core');
    var AbstractController = require('web.AbstractController');
    var BasicController = require('web.BasicController');
    var Domain = require('web.Domain');

    var _t = core._t;
    var qweb = core.qweb;

    var MapController = AbstractController.extend({
        /**
         * @override
         * @param {Object} params
         */
        init: function (parent, model, renderer, params) {
            this._super.apply(this, arguments);
        },
        reload: function (params) {
            return this._super.apply(this, arguments);
        },
    });

    return MapController;
});