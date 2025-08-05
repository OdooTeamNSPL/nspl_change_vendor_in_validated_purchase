from odoo import models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_change_vendor(self):
        return {
            'name': 'Change Vendor',
            'type': 'ir.actions.act_window',
            'res_model': 'change.vendor.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id}
        }
