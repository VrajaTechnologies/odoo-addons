# Copyright NuoBiT Solutions, S.L. (<https://www.nuobit.com>)
# Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_barcode_scan(self):
        action = super(StockPicking, self).action_barcode_scan()
        action['context']['default_picking_type_id'] = self.picking_type_id.id
        return action
