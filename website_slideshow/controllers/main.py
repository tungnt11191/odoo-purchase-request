# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import logging
import werkzeug

from odoo import http, _
from odoo.exceptions import AccessError, UserError
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom

_logger = logging.getLogger(__name__)


class WebsiteSlideshows(http.Controller):

    @http.route('/website_slideshow/get_slideshow', type='json', auth="public", website=True)
    def get_slideshow(self, slide_name):
        slide = request.env['s.slide.slide'].search([('name', '=', slide_name)])
        return slide.script