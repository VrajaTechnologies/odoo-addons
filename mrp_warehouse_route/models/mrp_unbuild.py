# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models

class MrpUnbuild(models.Model):
    _inherit = "mrp.unbuild"

    def _generate_consume_moves(self):
        moves = self.env['stock.move']
        for unbuild in self:
            move = self.env['stock.move'].create({
                'name': unbuild.name,
                'date': unbuild.create_date,
                'product_id': unbuild.product_id.id,
                'product_uom': unbuild.product_uom_id.id,
                'product_uom_qty': unbuild.product_qty,
                'location_id': unbuild.location_id.id,
                'location_dest_id': unbuild.product_id.property_stock_production.id,
                'origin': unbuild.name,
                'consume_unbuild_id': unbuild.id,
                'warehouse_id': unbuild.location_id.get_warehouse().id,
            })
            move._action_confirm()
            moves += move
        return moves

    def _generate_move_from_raw_moves(self, raw_move, factor):
        return self.env['stock.move'].create({
            'name': self.name,
            'date': self.create_date,
            'product_id': raw_move.product_id.id,
            'product_uom_qty': raw_move.product_uom_qty * factor,
            'product_uom': raw_move.product_uom.id,
            'procure_method': 'make_to_stock',
            'location_dest_id': self.location_dest_id.id,
            'location_id': raw_move.location_dest_id.id,
            'unbuild_id': self.id,
            'warehouse_id': self.location_dest_id.get_warehouse().id,
        })

    def _generate_move_from_bom_line(self, bom_line, quantity):
        return self.env['stock.move'].create({
            'name': self.name,
            'date': self.create_date,
            'bom_line_id': bom_line.id,
            'product_id': bom_line.product_id.id,
            'product_uom_qty': quantity,
            'product_uom': bom_line.product_uom_id.id,
            'procure_method': 'make_to_stock',
            'location_dest_id': self.location_dest_id.id,
            'location_id': self.product_id.property_stock_production.id,
            'unbuild_id': self.id,
            'warehouse_id': self.location_dest_id.get_warehouse().id,
        })