# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2016 hulshof#    #
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

class claim(models.Model):
    _name = "claim"
    _inherit = ['mail.thread']
    _description = "Claim"
    _order = "id desc"
    _track = {
        'Teruggaaf': {
        },
    }

    @api.one
    @api.depends('claim_line.amount_nett', 'claim_line.amount_tax','claim_line.amount_total', 'tax_return_line.amount_tax_return_total',
                 'cost_line.amount_cost', 'payment_line.amount_payment'
                 )
    def _compute_amount(self):
        self.amount_nett = sum(line.amount_nett for line in self.claim_line)
        self.amount_tax_orig = sum(line.amount_tax for line in self.claim_line)
        self.amount_tax_return = sum(line.amount_tax_return_total for line in self.tax_return_line)
        self.amount_tax = self.amount_tax_orig + self.amount_tax_return
        self.amount_cost = sum(line.amount_cost for line in self.cost_line)
        self.amount_total = sum(line.amount_total for line in self.claim_line)
        self.amount_payment = sum(line.amount_payment for line in self.payment_line)
        self.grand_total = self.amount_tax + self.amount_cost + self.amount_nett + self.amount_payment


    @api.one
    @api.depends('claim_line.amount_nett', 'claim_line.amount_tax','claim_line.amount_total', 'tax_return_line.amount_tax_return_total',
                 'cost_line.amount_cost', 'payment_line.amount_payment'
                 )
    def _compute_date(self):
        self.due_date = (line.due_date for line in self.claim_line)


    name = fields.Char(
        string=_("Name"),
        required=False,
        translate=True,
        readonly=False,
        size=64,
    )
    batchcode = fields.Char(
        string=_("Afstemcode"),
        required=True,
        translate=False,
        readonly=False,
        size=64
    )
    claim_line = fields.One2many('claim.line', 'claim_id',
        string=_("Claim Line"),
        required=False,
        translate=False,
        readonly=False,
        copy=True
    )
    cost_line = fields.One2many('cost.line', 'claim_id',
        string=_("Cost Lines"),
        required=False,
        translate=False,
        readonly=False,
        copy=True
    )
    tax_return_line = fields.One2many('tax.return.line', 'claim_id',
        string=_("Tax Return Line"),
        required=False,
        translate=False,
        readonly=False,
        copy=True
    )
    payment_line = fields.One2many('payment.line', 'claim_id',
        string=_("Payment Line"),
        required=False,
        translate=False,
        readonly=False,
        copy=True
    )
    zpartner = fields.Char(
        string=_("Debtor"),
        required=True,
        translate=False,
        readonly=False,
        size=64,
    )
    partnersrt = fields.Selection([
            ('CM','Consument'),
            ('KZM','Kein Zakelijk'),
        ],
        string='Debtor Type',
        required=True,
        translate=False,
        readonly=False
    )
    contrrek = fields.Char(
        string=_("Contract"),
        required=True,
        translate=False,
        readonly=False,
        size=64,
    )
    tax_return_sent = fields.Boolean(
        string=_("Teruggaaf"),
        readonly=True,
        default=False,
        copy=False,
        help="It indicates that the tax return has been sent."
        )
    comment = fields.Text('Additional Information'
        )
    amount_nett = fields.Float(
        string='Nett Claim Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_tax_orig = fields.Float(
        string='Tax Claim Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_total = fields.Float(
        string='Claim Original Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    grand_total = fields.Float(
        string='Claim Grand Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_tax_return = fields.Float(
        string='Tax Return',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_tax = fields.Float(
        string='Tax Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_cost = fields.Float(
        string='Collection Cost',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_payment = fields.Float(
        string='Payment',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    due_date = fields.Date(
        string=_("Due Date"),
        required=True,
        translate=False,
        readonly=False,
        store=True,
        compute='_compute_date'
    )