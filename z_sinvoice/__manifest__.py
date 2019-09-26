# -*- coding: utf-8 -*-
{
    'name': 'Hoa don dien tu',
    'version': '1.0',
    'author': 'tung.tung11191@gmail.com',
    'website': 'http://tungnt.dev',
    'category': 'accounting',
    'summary': 'Hoa don dien tu',
    'description': """
Hoa don dien tu
""",
    'depends': ['base','base_setup', 'mail', 'account','stock','z_invoice_template'],
    'data': [
        'security/s_invoice_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/res_country_views.xml',
        'views/account_invoice_views.xml',
        'views/stock_picking_views.xml',
        'views/res_config.xml',
        'data/data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
