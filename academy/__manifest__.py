# -*- coding: utf-8 -*-
{
     'name': "academy",

     'summary': """Manage trainings""",

     'description': """
       Open Academy module for managing trainings:
           - training courses
           - training sessions
           - attendees registration
   """,

     'author': "My Company",
     'website': "http://www.yourcompany.com",

     # Categories can be used to filter modules in modules listing
     # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
     # for the full list
     'category': 'Uncategorized',
     'version': '0.1',

     # any module necessary for this one to work correctly
     'depends': ['base', 'board', 'mail', 'website', 'account', 'stock'],

     # always loaded
     'data': [
        'security/ir.model.access.csv',
        'views/course_views.xml',
        'views/session_views.xml',
        'views/wizard_views.xml',
        'views/partner_views.xml',
        'views/session_board.xml',
        'reports.xml',
        'views/templates.xml',
        'data/data.xml',
        'views/import_stock.xml',

     ],
     # only loaded in demonstration mode
     'demo': [
        'demo/demo.xml',
     ],
}
