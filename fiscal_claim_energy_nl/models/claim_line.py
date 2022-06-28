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

from odoo import models, fields, api, _
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp

class claim_line(models.Model):
    _name = "claim.line"


    @api.depends('nett_amount', 'vat', 'energy_tax_e', 'energy_tax_g',
        'durable_tax_e', 'durable_tax_g')
    def _compute_amount(self):
        for line in self:
            line.amount_tax = line.vat + line.energy_tax_e + line.energy_tax_g + line.durable_tax_e + line.durable_tax_g
            line.amount_nett = line.nett_amount
            line.amount_total = line.amount_tax + line.amount_nett

    bdn = fields.Char(
        string=_("BdN"),
        required=True,
        translate=False,
        readonly=False,
        size=16,
    )
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
    contract_number = fields.Char(
        related='claim_id.contrrek',
        string='Contract',
        store=True
    )
    amount_tax = fields.Float(
        string='Tax',
        digits='claim',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_nett = fields.Float(
        string='Nett',
        digits='claim',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_total = fields.Float(
        string='Total',
        digits='claim',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    nett_amount = fields.Float(
        string=_("Nett Amount"),
        required=False,
        translate=False,
        readonly=False
    )
    due_date = fields.Date(
        string=_("Due Date"),
        required=True,
        translate=False,
        readonly=False
    )
    energy_tax_g = fields.Float(
        string=_("EB_G"),
        required=False,
        translate=False,
        readonly=False
    )
    docsoort = fields.Selection([
            ('DF','Hoofdsom'),
            ('EF','Kweenie1'),
            ('SF','Kweenie2'),
            ('AB','Kweenie3'),
            ('BA', 'Kweenie4'),
            ('KS','Incasso kosten'),
            ('FA','Correctie'),
        ],
        string=_("Document Type"),
        required=True,
        translate=False,
        readonly=False
    )
    durable_tax_e = fields.Float(
        string=_("Durable Tax E"),
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
    durable_tax_g = fields.Float(
        string=_("Durable Tax G"),
        required=False,
        translate=False,
        readonly=False
    )
    vat = fields.Float(
        string=_("VAT"),
        required=False,
        translate=False,
        readonly=False
    )
    docnr = fields.Char(
        string=_("Document Nr"),
        required=True,
        translate=False,
        readonly=False,
        size=32,
    )
    energy_tax_e = fields.Float(
        string=_("EB_E"),
        required=False,
        translate=False,
        readonly=False
    )


class cost_line(models.Model):
    _name = "cost.line"


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
    contract_number = fields.Char(
        related='claim_id.contrrek',
        string='Contract',
        store=True,
        readonly=True
    )
    amount_cost = fields.Float(
        string='Cost',
        digits='claim',
        readonly=False,
    )
    due_date = fields.Date(
        string=_("Due Date"),
        required=True,
        translate=False,
        readonly=False
    )
    docsoort = fields.Selection([
            ('KS','Incasso kosten?'),
            ('IR', 'Interest'),
        ],
        string=_("Document Type"),
        required=True,
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
    docnr = fields.Char(
        string=_("Document Nr"),
        required=True,
        translate=False,
        readonly=False,
        size=32,
    )

class payment_line(models.Model):
    _name = "payment.line"


    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Gives the sequence of this line when displaying the Payment Line."
    )
    claim_id = fields.Many2one('claim',
        string='Claim Reference',
        ondelete='cascade',
        index=True
    )
    contract_number = fields.Char(
        related='claim_id.contrrek',
        string='Contract',
        store=True,
        readonly=True
    )
    amount_payment = fields.Float(
        string='Payment',
        digits='claim',
        store=True,
        readonly=False,
    )
    date_payment = fields.Date(
        string=_("Date Payment"),
        required=True,
        translate=False,
        readonly=False
    )
    docsoort = fields.Selection([
            ('PM','Payment?'),
        ],
        string=_("Document Type"),
        required=True,
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
    docnr = fields.Char(
        string=_("Document Nr"),
        required=True,
        translate=False,
        readonly=False,
        size=32,
    )