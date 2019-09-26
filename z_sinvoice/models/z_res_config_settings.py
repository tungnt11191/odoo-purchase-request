# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval

from odoo import api, fields, models
from .constant import Constant

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    x_supplier_tax_code = fields.Char(string='Supplier Tax Code', config_parameter='z_sinvoice_for_dap.supplier_tax_code', default=Constant.SUPPLIER_TAX_CODE)
    x_sinvoice_uri = fields.Char(string='SINVOICE URI', config_parameter='z_sinvoice_for_dap.sinvoice_uri', default=Constant.SINVOICE_URI)
    x_sinvoice_create_uri = fields.Char(string='SINVOICE CREATE URI', config_parameter='z_sinvoice_for_dap.sinvoice_create_uri', default=Constant.SINVOICE_CREATE_URI)
    x_sinvoice_create_draft_uri = fields.Char(string='SINVOICE CREATE DRAFT URI', config_parameter='z_sinvoice_for_dap.sinvoice_create_draft_uri', default=Constant.SINVOICE_CREATE_DRAFT_URI)
    x_sinvoice_cancel_uri = fields.Char(string='SINVOICE CANCEL URI', config_parameter='z_sinvoice_for_dap.sinvoice_cancel_uri', default=Constant.SINVOICE_CANCEL_URI)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res.update(
            x_supplier_tax_code=ICPSudo.get_param('z_sinvoice_for_dap.supplier_tax_code', default=Constant.SUPPLIER_TAX_CODE),
            x_sinvoice_uri=ICPSudo.get_param('z_sinvoice_for_dap.sinvoice_uri', default=Constant.SINVOICE_URI),
            x_sinvoice_create_uri=ICPSudo.get_param('z_sinvoice_for_dap.sinvoice_create_uri', default=Constant.SINVOICE_CREATE_URI),
            x_sinvoice_create_draft_uri=ICPSudo.get_param('z_sinvoice_for_dap.sinvoice_create_draft_uri', default=Constant.SINVOICE_CREATE_DRAFT_URI),
            x_sinvoice_cancel_uri=ICPSudo.get_param('z_sinvoice_for_dap.sinvoice_cancel_uri', default=Constant.SINVOICE_CANCEL_URI),
        )
        return res

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('z_sinvoice_for_dap.supplier_tax_code', self.x_supplier_tax_code)
        self.env['ir.config_parameter'].sudo().set_param('z_sinvoice_for_dap.sinvoice_uri', self.x_sinvoice_uri)
        self.env['ir.config_parameter'].sudo().set_param('z_sinvoice_for_dap.sinvoice_create_uri', self.x_sinvoice_create_uri)
        self.env['ir.config_parameter'].sudo().set_param('z_sinvoice_for_dap.sinvoice_create_draft_uri', self.x_sinvoice_create_draft_uri)
        self.env['ir.config_parameter'].sudo().set_param('z_sinvoice_for_dap.sinvoice_cancel_uri', self.x_sinvoice_cancel_uri)
