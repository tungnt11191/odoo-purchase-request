# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import logging
import psycopg2

_logger = logging.getLogger(__name__)
class pos_order(models.Model):
    _inherit = "pos.order"

    @api.model
    def pre_create_from_ui(self, orders):
        # Keep only new orders
        submitted_references = [o['data']['name'] for o in orders]
        pos_order = self.search([('pos_reference', 'in', submitted_references)])
        existing_orders = pos_order.read(['pos_reference'])
        existing_references = set([o['pos_reference'] for o in existing_orders])
        orders_to_save = [o for o in orders if o['data']['name'] not in existing_references]
        order_ids = []

        for tmp_order in orders_to_save:
            to_invoice = tmp_order['to_invoice']
            order = tmp_order['data']
            if to_invoice:
                self._match_payment_to_invoice(order)
            pos_order = self._process_order(order)
            order_ids.append(pos_order.id)

        return order_ids

    @api.multi
    def action_pos_order_confirm(self):
        self.post_create_from_ui(self)

    @api.model
    def post_create_from_ui(self, orders):
        for pos_order in orders:
            try:
                pos_order.action_pos_order_paid()
            except psycopg2.OperationalError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))