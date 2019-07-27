# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import copy
import logging
from lxml import etree, html

from odoo.exceptions import AccessError
from odoo import api, fields, models
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    type = fields.Selection(selection_add=[('gmap', 'Map')])
