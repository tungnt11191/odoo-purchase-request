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

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):

    _inherit = ["crm.lead"]

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