# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    x_sinvoice_username = fields.Char(u'Tài khoản đăng nhập')
    x_sinvoice_password = fields.Char(u'Mật khẩu')
