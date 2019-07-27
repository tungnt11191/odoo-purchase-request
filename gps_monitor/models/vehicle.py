# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _


class Vehicle(models.Model):
    _inherit = 'mail.thread'
    _name = 'gps_monitor.vehicle'
    _description = 'Information on a vehicle'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
