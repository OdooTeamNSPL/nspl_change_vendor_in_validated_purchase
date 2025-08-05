from odoo import models, fields, api

class ChangeVendorWizard(models.TransientModel):
    _name = 'change.vendor.wizard'
    _description = 'Change Vendor Wizard'

    partner_id = fields.Many2one(
        'res.partner',
        string="New Vendor",
        required=True,
        domain=[('supplier_rank', '>', 0)])

    def confirm_change(self):
        active_id = self.env.context.get('active_id')
        purchase = self.env['purchase.order'].browse(active_id)

        if not purchase:
            return {'type': 'ir.actions.act_window_close'}

        purchase.write({'partner_id': self.partner_id.id})

        receipts = self.env['stock.picking'].search([('purchase_id', '=', purchase.id)])
        receipts.write({'partner_id': self.partner_id.id})

        bills = self.env['account.move'].search([
            ('purchase_id', '=', purchase.id),
            ('move_type', '=', 'in_invoice')
        ])

        for bill in bills:
            was_posted = bill.state == 'posted'
            if was_posted:
                bill.button_draft()

            bill.write({'partner_id': self.partner_id.id})

            if not bill.invoice_date:
                bill.invoice_date = fields.Date.today()

            if not bill.invoice_line_ids:
                expense_account = self.env['account.account'].search(
                    [('account_type', '=', 'expense')],
                    limit=1
                )
                if expense_account:
                    bill.write({
                        'invoice_line_ids': [(0, 0, {
                            'name': 'Vendor Change Adjustment',
                            'quantity': 1,
                            'price_unit': 0.0,
                            'account_id': expense_account.id
                        })]
                    })

            if was_posted:
                bill.action_post()

            bill.line_ids.write({'partner_id': self.partner_id.id})

        payments = self.env['account.payment'].search([('move_id', 'in', bills.ids)])
        for payment in payments:
            was_posted = payment.state == 'posted'
            if was_posted:
                payment.button_draft()
            payment.write({'partner_id': self.partner_id.id})
            if was_posted:
                payment.action_post()

        return {'type': 'ir.actions.act_window_close'}
