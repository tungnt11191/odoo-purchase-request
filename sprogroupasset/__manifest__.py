# -*- coding: utf-8 -*-

{

    'name': 'Company Equipments Management',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
        Track equipment and manage sprogroupasset requests.""",
    'author': 'tung.tung11191@gmail.com',
    'summary': 'Equipments Management',
    'depends': ['mail','hr'],
    'website': 'http://sprogroup.com',
    'images': ['static/description/icon.png'],
    'data': [
        'security/sprogroupasset.xml',
        'security/ir.model.access.csv',
        'data/sprogroupasset_data.xml',
        'views/sprogroupasset_borrow_views.xml',
        'views/sprogroupasset_provide_views.xml',
        'views/sprogroupasset_views.xml',
        'views/sprogroupasset_templates.xml',
        'views/sprogroupasset_vendor_views.xml',
        'views/sprogroupasset_inventory_views.xml',
        'models/wizard/export_view.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 105,
    'license': 'AGPL-3',
}
