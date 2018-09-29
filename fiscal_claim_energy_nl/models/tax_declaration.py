# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2018 hulshof#    #
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class TaxDeclaration(models.Model):
    _name = "tax.declaration"

    @api.one
    @api.depends('tax_return_line.amount_tax_return_total')
    def _compute_amount(self):
        self.vat_return = vat_return = sum(line.vat_return for line in self.tax_return_line)
        self.total_tax_return = total_tax_return = sum(line.amount_tax_return_total for line in self.tax_return_line)
        self.e_tax_return = total_tax_return - vat_return


    name = fields.Char('Description')
    comment = fields.Text('Note')
    from_invoice_date = fields.Date('From Claim Line Date', default='2000-01-01')
    to_invoice_date = fields.Date('To Claim Line Date', default=False)
    from_batch_date = fields.Date('From Batch Date', default='2000-01-01')
    to_batch_date = fields.Date('To Batch Date', default=False)
    date_tax_request = fields.Date('Date Tax Request', default=fields.Date.today)
    cutoff = fields.Selection([
                                ('line_date', 'Claim Line Date'),
                                ('last_line', 'Last Line Date'),
                                ], string='Cutoff Concept', copy=False, store=True, default='line_date'
                             )
    state = fields.Selection([
                                ('draft', 'Draft'),
                                ('submitted', 'Submitted'),
                                ('accepted', 'Accepted'),
                                ('cancel', 'Cancelled'),
                                ], string='State', readonly=True, copy=False, store=True, default='draft'
                            )
    tax_return_line = fields.One2many('tax.return.line', 'declaration_id',
                                      string=_("Tax Line"),
                                      required=False,
                                      translate=False,
                                      readonly=False,
                                      copy=False,
                                      track_visibility='onchange',
                                      )
    vat_return = fields.Float(string='Vat Return',
                            digits=dp.get_precision('claim'),
                            store=True,
                            readonly=True,
                            compute='_compute_amount')
    e_tax_return = fields.Float(string='E Tax Return',
                              digits=dp.get_precision('claim'),
                              store=True,
                              readonly=True,
                              compute='_compute_amount')
    total_tax_return = fields.Float(string='Total Tax Return',
                                digits=dp.get_precision('claim'),
                                store=True,
                                readonly=True,
                                compute='_compute_amount')


    @api.multi
    @api.constrains('from_invoice_date', 'to_invoice_date', 'from_batch_date', 'to_batch_date')
    def _check_start_end_dates(self):
        for record in self:
            if record.from_invoice_date and record.to_invoice_date \
                    and record.from_invoice_date > record.to_invoice_date:
                raise ValidationError(_(
                    'The from claim line date is after the to date!'))
            if record.from_batch_date and record.to_batch_date \
                    and record.from_batch_date > record.to_batch_date:
                raise ValidationError(_(
                    'The from batch date is after the to batch date!'))



class tax_return_line(models.Model):
    _name = "tax.return.line"

    @api.one
    @api.depends('vat_return', 'energy_tax_e_return', 'energy_tax_g_return',
        'durable_tax_e_return', 'durable_tax_g_return')
    def _compute_amount(self):
        #import pdb; pdb.set_trace()
        self.amount_tax_return_total = self.vat_return + self.energy_tax_e_return + self.energy_tax_g_return + self.durable_tax_e_return + self.durable_tax_g_return



    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Gives the sequence of this line when displaying the invoice."
    )
    claim_id = fields.Many2one('claim',
        string='Claim Reference',
        ondelete='cascade',
        index=True
    )
    declaration_id = fields.Many2one('tax.declaration',
                               string='Tax Declaration',
                               ondelete='cascade',
                               index=True
                               )
    batch_date = fields.Date(
        string=_("Date Claim Batch"),
        related='claim_id.claim_date',
        translate=False,
        readonly=True,
        store=True
    )
    batchcode = fields.Char(
        string=_("Code Claim Batch"),
        related='claim_id.batchcode',
        translate=False,
        readonly=True,
        store=True
    )
    contract_number = fields.Char(
        related='claim_id.contrrek',
        string='Contract',
        store=True,
        readonly=True
    )
    amount_tax_return_total= fields.Float(
        string='Tax',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    date_tax_request = fields.Date(
        string=_("Date Tax Request"),
        required=True,
        translate=False,
        readonly=False
    )
    energy_tax_g_return = fields.Float(
        string=_("Energy Tax G Return"),
        required=False,
        translate=False,
        readonly=False
    )
    docsoort = fields.Selection([
            ('TR','Tax Return'),
            ('TD','Tax Declaration'),
        ],
        string=_("Document Type"),
        required=True,
        translate=False,
        readonly=False
    )
    durable_tax_e_return = fields.Float(
        string=_("Durable Tax E Return"),
        required=False,
        translate=False,
        readonly=False
    )
    ref = fields.Char(
        string=_("Reference"),
        required=False,
        translate=False,
        readonly=False,
        size=64,
    )
    durable_tax_g_return = fields.Float(
        string=_("Durable Tax G Return"),
        required=False,
        translate=False,
        readonly=False
    )
    vat_return = fields.Float(
        string=_("VAT Return"),
        required=False,
        translate=False,
        readonly=False
    )
    docnr = fields.Char(
        string=_("Document Nr"),
        required=False,
        translate=False,
        readonly=False,
        size=32,
    )
    energy_tax_e_return = fields.Float(
        string=_("Energy Tax E Return"),
        required=False,
        translate=False,
        readonly=False
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('cancel', 'Cancelled'),
    ],
        string='Tax Line Status',
        related='declaration_id.state',
        readonly=True,
        copy=False,
        store=True,
        default='draft'
    )

