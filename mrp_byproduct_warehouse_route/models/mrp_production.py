# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class MrpProduction(models.Model):
    _description = 'Production'
    _inherit = 'mrp.production'

    def _create_byproduct_move(self, sub_product):
        Move = self.env['stock.move']
        for production in self:
            source = production.product_id.property_stock_production.id
            product_uom_factor = production.product_uom_id._compute_quantity(production.product_qty - production.qty_produced, production.bom_id.product_uom_id)
            qty1 = sub_product.product_qty
            qty1 *= product_uom_factor / production.bom_id.product_qty
            data = {
                'name': 'PROD:%s' % production.name,
                'date': production.date_planned_start,
                'product_id': sub_product.product_id.id,
                'product_uom_qty': qty1,
                'product_uom': sub_product.product_uom_id.id,
                'location_id': source,
                'location_dest_id': production.location_dest_id.id,
                'operation_id': sub_product.operation_id.id,
                'production_id': production.id,
                'origin': production.name,
                'unit_factor': qty1 / (production.product_qty - production.qty_produced),
                'subproduct_id': sub_product.id,
                'warehouse_id': production.location_dest_id.get_warehouse().id,
            }
            move = Move.create(data)
            move._action_confirm()