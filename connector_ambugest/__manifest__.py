# -*- coding: utf-8 -*-
# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': "Ambugest connector",
    'description': "Connect Odoo with Ambugest",
    'version': '10.0.0.1.0',
    'author': 'NuoBiT Solutions, S.L., Eric Antones',
    'license': 'AGPL-3',
    'category': 'Connector',
    'website': 'https://www.nuobit.com',
    'depends': ['connector'],
    'data': [
        'views/ir_translation_views.xml',
    ],
    'external_dependencies': {
        'python': [],
    },
    'installable': True,
}
