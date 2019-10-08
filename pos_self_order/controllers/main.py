# -*- coding: utf-8 -*-
import json
import logging
import werkzeug.utils

from odoo import http
from odoo.http import request
from odoo import fields
_logger = logging.getLogger(__name__)


class PosSelfController(http.Controller):

    def generate_unique_id(self, pos_session,sequence_number):
        def zero_pad(num,size):
            s = ""+str(num)
            while (len(s) < size):
                s = "0" + str(s)
            return s;
        return str(zero_pad(pos_session.id, 5)) + '-' + str(zero_pad(pos_session.login_number, 3)) + '-' + str(zero_pad(sequence_number, 4))

    @http.route('/customer/pos/web', type='http', auth='public')
    def pos_web(self, debug=False, **k):
        # if user not logged in, log him in
        context = {
            'session_info': json.dumps(request.env['ir.http'].session_info())
        }
        return request.render('pos_self_order.index', qcontext=context)

    @http.route(['/customer/pos/category'], type='http', auth='public', methods=['GET'])
    def get_pos_category(self, **kw):
        pos_categories = request.env['pos.category'].sudo().search([])
        out_put = {
            'status': True,
            'categories': []
        }
        for cat in pos_categories:
            out_put['categories'].append({'id':cat.id,'name':cat.name})

        return json.dumps(out_put)

    @http.route(['/customer/pos/product'], type='http', auth='public', methods=['GET'])
    def get_pos_product(self, category_id, **kw):
        domain = []
        category_id = int(category_id)
        if category_id != 0:
            domain.append(('pos_categ_id', '=', category_id))

        domain.append(('available_in_pos', '=', True))
        pos_products = request.env['product.product'].sudo().search(domain)
        out_put = {
            'status': True,
            'products': []
        }
        for p in pos_products:
            product = p.read()
            out_put['products'].append(product[0])

        return json.dumps(out_put)

    @http.route(['/customer/pos/order/create'], type='json', auth='public', methods=['POST'])
    def create_pos_order(self, order, **kwargs):
        # get customer
        customer = order.get('customer')
        exited_customer = request.env['res.partner'].sudo().search([('name', '=',customer.get('customer_name'))], limit=1)
        if len(exited_customer.ids) > 0:
            ordered_customer = exited_customer
        else:
            ordered_customer = request.env['res.partner'].sudo().create({'name':customer.get('customer_name')})

        # get table
        exited_table = request.env['restaurant.table'].sudo().search([('security_code', '=', customer.get('security_code'))], limit=1)
        if len(exited_table.ids) > 0:
            ordered_table = exited_table
        else:
            return False
        """
        Simulation of sales coming from the interface, even after closing the session
        """
        portal_user = request.env['res.users'].sudo().browse(7)
        main_pos_config = exited_table.config_id
        current_session = main_pos_config.current_session_id

        FROMPRODUCT = object()

        def compute_tax(product, price, taxes=FROMPRODUCT, qty=1):
            if taxes is FROMPRODUCT:
                taxes = product.taxes_id
            currency = self.pos_config.pricelist_id.currency_id
            taxes = taxes.compute_all(price, currency, qty, product=product)['taxes']
            untax = price * qty
            return untax, sum(tax.get('amount', 0.0) for tax in taxes)

        # I click on create a new session button
        # self.pos_config.open_session_cb()

        # current_session = self.pos_config.current_session_id
        sequence_number = current_session.sequence_number + 1
        ref = self.generate_unique_id(pos_session=current_session, sequence_number = sequence_number)
        untax, atax = 20, 2
        carrot_order = {'data':
          {
           'amount_paid': untax + atax,
           'amount_return': 0,
           'amount_tax': atax,
           'amount_total': untax + atax,
           'creation_date': fields.Datetime.now(),
           'fiscal_position_id': False,
           'lines': [],
           'name': 'Order '+ref,
           'partner_id': ordered_customer.id,
           'table_id': ordered_table.id,
           'pos_session_id': current_session.id,
           'sequence_number': sequence_number,
           'statement_ids': [[0,0,
             {'account_id':  current_session.user_id.partner_id.property_account_receivable_id.id,
              'amount': untax + atax,
              'journal_id': main_pos_config.journal_ids[0].id,
              'name': fields.Datetime.now(),
              'statement_id': current_session.statement_ids[0].id}]],
           'uid': ref,
           'user_id': current_session.user_id.id

           },
          'id': ref,
          'to_invoice': False}

        amount_total = 0
        for line in order.get('order_line'):
            product = request.env['product.product'].sudo().browse(line.get('product_id'))
            amount_total += int(line.get('price_unit')) * int( line.get('quantity'))
            line_item = [0,0, {'discount': 0,
                  'pack_lot_ids': [],
                  'price_unit': line.get('price_unit'),
                  'product_id': product.id,
                  'qty': line.get('quantity'),
                  'tax_ids': [(6, 0, product.taxes_id.ids)]
              }]
            carrot_order['data']['lines'].append(line_item)
        carrot_order['data']['amount_total'] = amount_total
        carrot_order['data']['amount_paid'] = amount_total
        carrot_order['data']['statement_ids'][0][2]['amount'] = amount_total
        created_orders = request.env['pos.order'].sudo().pre_create_from_ui([carrot_order])
