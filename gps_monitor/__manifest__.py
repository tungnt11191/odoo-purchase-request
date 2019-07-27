# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'GPS monitor',
    'version' : '1.0',
    'sequence': 165,
    'category': 'Human Resources',
    'website' : 'http://tungnt.dev',
    'summary' : 'Vehicle,GPS tracking',
    'author' : 'tung.tung11191@gmail.com',
    'description' : """
    GPS monitor
""",
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/fleet_security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_views.xml',
        'views/vehicle_templates.xml',
        'views/res_config.xml',
    ],
    'qweb': ['static/src/xml/widget_places.xml'],
    'installable': True,
    'application': True,
}
