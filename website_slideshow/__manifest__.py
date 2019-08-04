# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Slideshow',
    'category': 'Website',
    'description': """
Slideshow.
========================

""",
    'version': '0.1',
    'depends': ['web','website','website_blog'],
    'data': [
        'views/assets.xml',
        'views/snippets.xml',
        'views/website_slides_backend.xml',
        'security/ir.model.access.csv',
    ],
    # 'qweb': [
    #     "static/src/xml/*.xml",
    # ],
    'auto_install': False
}
