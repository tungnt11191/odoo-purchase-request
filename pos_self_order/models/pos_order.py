# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import logging
import psycopg2
# from pos_self_order.pos_retail.controllers.pos_controllers import pos_bus

import odoo.tools as tools
import json
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

                value = {
                    'device_id': self._get_unique_number_pos_session(pos_order),
                    'action': 'set_state',
                    'data':{
                        'state': 'Waiting',
                        'uid': pos_order.pos_reference[6:] + '-0'
                    },
                    'bus_id': pos_order.config_id.bus_id.id,
                    'order_uid' : pos_order.pos_reference[6:]
                }
                message = {
                    'user_send_id': pos_order.user_id.id,
                    'value': value,
                }
                self.send(pos_order.config_id.bus_id.id, [message])
                # send to kitchen view
                # pos_buses = pos_bus()
                # pos_buses.send(1,2)
            except psycopg2.OperationalError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))


    def _get_unique_number_pos_session(self,order):
        return str(order.session_id.login_number) + '_' + str(order.config_id.id)

    @api.model
    def sync_from_customer(self, orders):
        for pos_order in orders:
            try:
                value = {
                    'action': 'new_order_from_customer',
                    'data': {
                        'state': 'Waiting',
                        'order' : pos_order
                    },
                    'order_uid' : pos_order.get('id')[6:]
                }
                message = {
                    'user_send_id': pos_order.get('data').get('user_id'),
                    'value': value,
                }
                self.send(pos_order.get('data').get('bus_id'), [message])
                # send to kitchen view
                # pos_buses = pos_bus()
                # pos_buses.send(1,2)
            except psycopg2.OperationalError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

    @api.multi
    def send(self, bus_id, messages):
        for message in messages:
            if not message.get('value', None) \
                    or not message['value'].get('order_uid', None) \
                    or not message['value'].get('action', None):
                continue
            self.env.cr.execute("SELECT user_id FROM pos_session WHERE state='opened' AND bus_id=%s" % (bus_id))
            users = self.env.cr.fetchall()
            if not users:
                return True
            for user in users:
                self.env['bus.bus'].sendmany(
                    [[(self.env.cr.dbname, 'pos.sync.sessions', user[0]), message]])
        return True