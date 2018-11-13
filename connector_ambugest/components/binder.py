# -*- coding: utf-8 -*-
# © 2013 Guewen Baconnier,Camptocamp SA,Akretion
# © 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.component.core import Component


class AmbugestModelBinder(Component):
    """ Bind records and give odoo/ambugest ids correspondence

    Binding models are models called ``ambugest.{normal_model}``,
    like ``ambugest.res.partner`` or ``ambugest.product.product``.
    They are ``_inherits`` of the normal models and contains
    the Ambugest ID, the ID of the Ambugest Backend and the additional
    fields belonging to the Ambugest instance.
    """
    _name = 'ambugest.binder'
    _inherit = ['base.binder', 'base.ambugest.connector']
    _apply_on = [
        'ambugest.sale.order',
        'ambugest.sale.order.line',
    ]
