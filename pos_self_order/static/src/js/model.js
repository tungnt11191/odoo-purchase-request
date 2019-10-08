/*
    This module create by: thanhchatvn@gmail.com
    License: OPL-1
    Please do not modification if i'm not accepted
 */
odoo.define('pos_self_order.model', function (require) {
    var models = require('point_of_sale.models');
    var utils = require('web.utils');
    var core = require('web.core');
    var round_pr = utils.round_precision;
    var _t = core._t;
    var rpc = require('pos.rpc');
    var big_data = require('pos_retail.big_data');
    var base = require('pos_retail.base');
    var session = require('web.session');
    var time = require('web.time');

    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
//        tungnt
        add_new_order_from_customer: function (data) {
            var self = this;
            _super_PosModel.add_new_order.apply(this, arguments);
            var order = this.get_order();

            var lines = data.value.data.order.data.lines;
            for (i = 0; i < lines.length; i++) {
                var line = lines[i][2];
                var product = self.db.get_product_by_id(line.product_id);
                var new_line = new models.Orderline({}, {pos: order.pos, order: order, product: product});
                new_line.set_quantity(line.qty, 'keep price');
                order.orderlines.add(new_line);
            }

            var client = order.get_client();
            if (!client) {
                var client_default = this.db.get_partner_by_id(data.value.data.order.data.partner_id);

                if (client_default && order) {
                    setTimeout(function () {
                        order.set_client(client_default);
                    }, 500);
                }
            }
        }
    });
});
