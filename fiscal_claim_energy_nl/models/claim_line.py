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

class claim_line(models.Model):
    _name = "claim.line"

    @api.one
    @api.depends('nett_amount', 'vat', 'energy_tax_e', 'energy_tax_g',
        'durable_tax_e', 'durable_tax_g')
    def _compute_amount(self):
        #import pdb; pdb.set_trace()
        self.amount_tax = self.vat + self.energy_tax_e + self.energy_tax_g + self.durable_tax_e + self.durable_tax_g
        self.amount_nett = self.nett_amount
        self.amount_total = self.amount_tax + self.amount_nett

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
    amount_tax = fields.Float(
        string='Tax',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_nett = fields.Float(
        string='Nett',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_total = fields.Float(
        string='Total',
        digits=dp.get_precision('claim'),
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
            ('DF','Hoofdsom?'),
            ('EF','Kweenie1'),
            ('SF','Kweenie2'),
            ('AB','Kweenie3'),
            ('KS','Incasso kosten?'),
            ('FA','Correctie?'),
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
        string=_("Energy Tax E Return"),
        required=False,
        translate=False,
        readonly=False
    )
    docsoort = fields.Selection([
            ('TR','Tax Return'),
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
    amount_cost = fields.Float(
        string='Cost',
        digits=dp.get_precision('claim'),
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
    amount_payment = fields.Float(
        string='Payment',
        digits=dp.get_precision('claim'),
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
        required=False,
        translate=False,
        readonly=False,
        size=32,
    )