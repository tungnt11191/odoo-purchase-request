# -*- coding: utf-8 -*-
{
    'name': 'Blog Post Category',
    'version': '1.0',
    'website': 'https://tungnt.dev',
    'category': 'Others',
    'summary': 'Blog Post Category',
    'author': 'tung.tung11191@gmail.com',
    'description': """
Blog Post Category
""",
    'depends': ['base_setup', 'mail','website_blog'],
    'data': [
        'security/blog_category_security.xml',
        'security/ir.model.access.csv',
        'views/blog_category_views.xml',
        'views/blog_post_views.xml',
        'views/blog_category_template.xml',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True
}
