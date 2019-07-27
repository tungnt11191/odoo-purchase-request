odoo.define('gps_monitor.MapModel', function(require) {
    'use strict';

    var AbstractModel = require('web.AbstractModel');
    var BasicModel = require('web.BasicModel');

    var MapModel = AbstractModel.extend({
        /**
         * @override
         */
        reload: function (id, options) {
            return this._super.apply(this, arguments);
        },
        /**
         * @override
         */
        load: function (params) {
            return this._super(params);
        },
        /**
         * Ensures that there is no nested groups in Map (only the first grouping
         * level is taken into account).
         *
         * @override
         */
        _readGroup: function (list) {
            return this._super.apply(this, arguments);
        },

    });

    return MapModel;

});
