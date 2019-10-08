# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class restaurant_table(models.Model):

    _inherit = "restaurant.table"

    security_code = fields.Char('Security code')
    order_state = fields.Selection([('available', 'Available'), ('in_occupied', 'In Occupied')], string='State')
    config_id = fields.Many2one('pos.config', string='Pos Config')


class pos_config(models.Model):

    _inherit = "pos.config"

    table_ids = fields.One2many('restaurant.table', 'config_id', string='Tables')
