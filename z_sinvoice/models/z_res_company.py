# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    x_ma_loai_hoa_don = fields.Char(u'Mã loại hóa đơn')
    x_loai_ky_gui = fields.Char(u'Mã loại ký gửi')
    x_ma_loai_van_chuyen_noi_bo = fields.Char(u'Mã loại vận chuyển nội bộ')
    x_ma_mau_hoa_don = fields.Char(u'Mã mẫu hóa đơn')
    x_ma_mau_ky_gui = fields.Char(u'Mã mẫu ký gửi')
    x_ma_mau_van_chuyen_noi_bo = fields.Char(u'Mã mẫu vận chuyển nội bộ')
