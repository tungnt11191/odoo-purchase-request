# -*- coding: utf-8 -*-

{

    'name': 'Google Map',
    'version': '1.0',
    'category': 'Extra Tools',
    'description': """
        Google Map widget.""",
    'author': 'tung.tung11191@gmail.com',
    'summary': 'Google Map widget',
    'images': ['static/description/icon.png'],
    'depends': ['base_setup'],
    'data': [
        'views/templates.xml',
        'views/res_config_views.xml'
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 105,
    'license': 'AGPL-3',
}
