# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import uuid
from itertools import groupby

from odoo import api, fields, models, _
from odoo import tools
from odoo.addons.http_routing.models.ir_http import url_for
from odoo.osv import expression
from odoo.http import request
from odoo.tools import pycompat

import operator
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = ["crm.lead"]

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            self.user_id = False
            users = self.env['res.users'].sudo().search([('company_ids', 'child_of', [self.company_id.id])])
            return {'domain': {'user_id': [('id', 'in', users.ids)]}}

    def open_action_crm_lead_change_company_n_staff(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'new',
            'view_id': self.env.ref('blog_category.view_change_crm_lead_simplified').id,
        }

    @api.multi
    def action_save_company_n_staff(self):
        for lead in self:
            test = True

    @api.onchange('user_id')
    def _onchange_user_id(self):
        """ When changing the user, also set a team_id or restrict team id to the ones user_id is member of. """
        if self.user_id.sudo().sale_team_id:
            values = self._onchange_user_values(self.user_id.id)
            self.update(values)


    @api.multi
    def write(self, vals):
        if('user_id' in vals and 'company_id' in vals):
            return super(CrmLead, self).write(vals)
        else:
            return super(CrmLead, self).write(vals)
class ResUsers(models.Model):

    _inherit = ["res.users"]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if(self.has_group('base.group_erp_manager')):
            ids = self.env['res.users'].sudo().search(args, limit=limit)
            # recs = self.browse(ids)
            return models.lazy_name_get(ids.sudo())
        else:
            return super(ResUsers, self).name_search(name, args=args, operator=operator, limit=limit)

