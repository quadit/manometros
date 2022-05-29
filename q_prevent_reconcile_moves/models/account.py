# Copyright 2022 - QUADIT, SA DE CV (https://www.quadit.mx)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit ='account.move'

    invoice_reversed = fields.Boolean('Invoice with credit note')
    invoice_origin_reverse_id = fields.Many2one('account.move', 'Invoice Origin')

class AccountMoveLine(models.Model):
    _inherit ='account.move.line'

    def _create_exchange_difference_move(self):
        has_invoice = False
        has_refund = False
        for line in self:
            if line.move_id.move_type in ('out_invoice', 'in_invoice'):
                has_invoice = True
            elif line.move_id.move_type in ('out_refund', 'in_refund'):
                has_refund = True
        if has_invoice and has_refund:
            return False
        return super(AccountMoveLine, self)._create_exchange_difference_move()

class AccountMoveReversal(models.TransientModel):
    _inherit = 'account.move.reversal'

    def _prepare_default_reversal(self, move):
        res = super(AccountMoveReversal, self)._prepare_default_reversal(move=move)
        move.invoice_reversed = True
        res.update({'invoice_origin_reverse_id': move.id})
        return res

class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    def _create_tax_cash_basis_moves(self):
        for partial in self:
            debit_move_type = partial.debit_move_id.move_id.move_type
            credit_move_type = partial.credit_move_id.move_id.move_type
            if debit_move_type == 'out_invoice' and credit_move_type == 'out_refund':
                return False
            elif credit_move_type == 'out_invoice' and debit_move_type == 'out_refund':
                return False
            elif debit_move_type == 'in_invoice' and credit_move_type == 'in_refund':
                return False
            elif credit_move_type == 'in_invoice' and debit_move_type == 'in_refund':
                return False
        return super(AccountPartialReconcile, self)._create_tax_cash_basis_moves()
