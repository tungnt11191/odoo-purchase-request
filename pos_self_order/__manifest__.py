# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'POS self order',
    'version' : '1.0',
    'sequence': 165,
    'category': 'Point of Sale',
    'website' : 'http://tungnt.dev',
    'summary' : 'POS self order',
    'description' : """
POS self order
""",
    'depends': [
        'pos_retail',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/restaurant_table.xml',
        'data/data.xml',
    ],
    'installable': True,
    'application': True,
}
