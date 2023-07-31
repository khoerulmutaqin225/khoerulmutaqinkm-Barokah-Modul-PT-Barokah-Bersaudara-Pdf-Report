# -*- coding: utf-8 -*-
{
    'name': "Barokah Module",

    'summary': """
        Modul Tambahan untuk Report""",

    'description': """
        Form tambahan untuk report pdf dan excel untuk pt Berkah bersaudara
    """,

    'author': "Khoerul Mutaqin",
    'website': "https://barokahperkasagroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail', 'stock', 'purchase'],

    # always loaded
    'data': [
        'views/stock_picking.xml',
        'wizard/create_approval.xml',
        'report/approval_stock_picking_report.xml',
        'security/stock_picking_inherit.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
