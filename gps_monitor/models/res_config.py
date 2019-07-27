# -*- coding: utf-8 -*-
# License AGPL-3
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_maps_view_api_key = fields.Char(string='Google Maps View Api Key')
    socket_io_server = fields.Char(string='Socket.io Server')

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param('gps_monitor.api_key_geocode', self.google_maps_view_api_key)
        ICPSudo.set_param('gps_monitor.socket_io_server', self.socket_io_server)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        res.update({
            'google_maps_view_api_key': ICPSudo.get_param('gps_monitor.api_key_geocode', default=''),
            'socket_io_server': ICPSudo.get_param('gps_monitor.socket_io_server', default=''),
        })
        return res
