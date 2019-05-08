# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict

from odoo import http, fields
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.tools import html2plaintext


class WebsitePopup(http.Controller):
    @http.route('/website_popup/load_country', type="json", auth="public", csrf=False)
    def load_countries(self,args):
        countries = request.env['res.country'].sudo().search([])
        output = {
            'countries' : []
        }
        for country in countries:
            output['countries'].append({'id':country.id,'name':country.name})

        return output

    @http.route('/website_popup/load_blog_category', type="json", auth="public", csrf=False)
    def load_categories(self, args):
        categories = request.env['blog.post.category'].sudo().search([])
        output = {
            'categories': []
        }
        for country in categories:
            output['categories'].append({'id': country.id, 'name': country.name})

        return output
