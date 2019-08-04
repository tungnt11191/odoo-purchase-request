# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import copy
import logging
from lxml import etree, html

from odoo.exceptions import AccessError
from odoo import api, fields, models
from odoo.tools import pycompat
from io import StringIO

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    @api.multi
    def save(self, value, xpath=None):
        super(IrUiView, self).save(value, xpath)
        arch_section = html.fromstring(value, parser=html.HTMLParser(encoding='utf-8'))
        # rev_slide_sections = arch_section.xpath('//section[hasclass("s_slideshow")]')
        slideshows = arch_section.xpath('//div[hasclass("tungnt_s_slideshow")]')
        root = arch_section.xpath('//*[@data-oe-model = "blog.post" or @data-oe-model = "ir.ui.view"]')

        if len(root) > 0:
            post_id = root[0].get('data-oe-id')
            model = root[0].get('data-oe-model')

            slide_name_array = []
            s_slide_model = self.env['s.slide.slide'].sudo()
            for el in slideshows:
                slide_name = el.get('id')
                slide_name_array.append(slide_name)
                s_slide = s_slide_model.search([('name', '=', slide_name)])
                page = self.env[model].browse(int(post_id))
                if len(s_slide.ids) == 0:
                    s_slide_model.create({'name': slide_name, 'source_id': int(post_id), 'model': model, 'source_name': page.name})

            delete_slide = s_slide_model.search([('name', 'not in', slide_name_array), ('source_id', '=', int(post_id)), ('model', '=', model)])
            delete_slide.unlink()

    def html_parse(self, value):
        parser = etree.HTMLParser(encoding='utf8')
        tree = etree.parse(StringIO(value), parser)
        return tree

