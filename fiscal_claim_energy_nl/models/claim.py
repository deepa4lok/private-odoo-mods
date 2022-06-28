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
from odoo.exceptions import UserError, ValidationError
from odoo.addons.queue_job.job import Job #, related_action
from odoo.addons.queue_job.exception import FailedJobError

class claim(models.Model):
    _name = "claim"
    _inherit = ['mail.thread']
    _description = "Claim"
    _order = "id desc"
    _track = {
        'Teruggaaf': {
        },
    }


    @api.depends('claim_line',
                 'tax_return_line',
                 'cost_line',
                 'payment_line'
                 )
    def _compute_amount(self):
        # self.ensure_one()
        ## parsing claim/payment/cost/tax lines in originating variables

        for case in self:
            case.orig_tax = var_orig_tax = sum(line.amount_tax for line in case.claim_line)
            case.orig_vat = var_orig_vat = sum(line.vat for line in case.claim_line)
            case.orig_energy_tax_e = var_orig_energy_tax_e = sum(line.energy_tax_e for line in case.claim_line)
            case.orig_durable_tax_e = var_orig_durable_tax_e = sum(line.durable_tax_e for line in case.claim_line)
            case.orig_energy_tax_g = var_orig_energy_tax_g = sum(line.energy_tax_g for line in case.claim_line)
            case.orig_durable_tax_g = var_orig_durable_tax_g = sum(line.durable_tax_g for line in case.claim_line)
            case.orig_amount_nett = var_orig_amount_nett = sum(line.amount_nett for line in case.claim_line)
            case.orig_amount_total = var_orig_amount_total = sum(line.amount_total for line in case.claim_line)
            case.amount_cost_lines = var_amount_cost_lines = sum(line.amount_cost for line in case.cost_line)
            case.amount_payment_lines = var_amount_payment_lines = sum(line.amount_payment for line in case.payment_line)
            case.tax_return_lines_total = var_tax_return_lines_total = \
                sum(line.amount_tax_return_total for line in case.tax_return_line)
            case.tax_return_lines_ee = var_tax_return_lines_ee = \
                sum(line.energy_tax_e_return for line in case.tax_return_line)
            case.tax_return_lines_de = var_tax_return_lines_de = \
                sum(line.durable_tax_e_return for line in case.tax_return_line)
            case.tax_return_lines_eg = var_tax_return_lines_eg = \
                sum(line.energy_tax_g_return for line in case.tax_return_line)
            case.tax_return_lines_dg = var_tax_return_lines_dg = \
                sum(line.durable_tax_g_return for line in case.tax_return_line)
            case.tax_return_lines_vat = var_tax_return_lines_vat = \
                sum(line.vat_return for line in case.tax_return_line)
            ## calculating original combined values
            case.orig_nett_tax_total = var_orig_nett_tax_total = var_orig_tax + var_orig_amount_nett
            case.orig_e_tax = var_orig_e_tax = var_orig_energy_tax_e + var_orig_durable_tax_e
            case.orig_g_tax = var_orig_g_tax = var_orig_durable_tax_g + var_orig_energy_tax_g
            case.orig_energy_tax = var_orig_energy_tax = var_orig_energy_tax_e + var_orig_energy_tax_g
            case.orig_ode_tax = var_orig_ode_tax = var_orig_durable_tax_e + var_orig_durable_tax_g
            case.orig_energy_ode_tax = var_orig_energy_ode_tax = var_orig_energy_tax + var_orig_ode_tax
            case.total_claim_incl_cost = var_total_claim_incl_cost = var_orig_nett_tax_total + var_amount_cost_lines
            case.total_claim_minus_payments = var_total_claim_incl_cost - var_amount_payment_lines


            ## todo calculated amounts: leaving out negative amounts. test is if orig_energy_ode_tax is positive.
            ## todo Is this right?
            case.calc_amount_vat = var_calc_amount_vat = var_orig_vat if var_orig_vat > 0 else 0
            case.calc_amount_energy_tax_e = var_calc_amount_energy_tax_e = \
                var_orig_energy_tax_e if var_orig_energy_ode_tax > 0 else 0
            case.calc_amount_durable_tax_e = var_calc_amount_durable_tax_e = \
                var_orig_durable_tax_e if var_orig_energy_ode_tax > 0 else 0
            case.calc_amount_energy_tax_g = var_calc_amount_energy_tax_g = \
                var_orig_energy_tax_g if var_orig_energy_ode_tax > 0 else 0
            case.calc_amount_durable_tax_g = var_calc_amount_durable_tax_g = \
                var_orig_durable_tax_g if var_orig_energy_ode_tax > 0 else 0
            ## calculating calculated combined values, throwing out negative amounts


            # Fixme: Can be removed -- deep
            # case.calc_amount_e_tax = var_calc_amount_e_tax = var_calc_amount_energy_tax_e + var_calc_amount_durable_tax_e -- deep
            # case.calc_amount_g_tax = var_calc_amount_g_tax = var_calc_amount_durable_tax_g + var_calc_amount_energy_tax_g -- deep
            # Fixme: -- end --


            case.calc_amount_energy_tax = var_calc_amount_energy_tax = var_calc_amount_energy_tax_e + var_calc_amount_energy_tax_g


            # Fixme: remove it -- deep
            # case.calc_amount_ode_tax = var_calc_amount_ode_tax = var_calc_amount_durable_tax_e + var_calc_amount_durable_tax_g --deep
            # case.calc_amount_energy_ode_tax = var_calc_amount_energy_ode_tax = var_calc_amount_energy_tax_e + \
            #                                                  var_calc_amount_durable_tax_e + \
            #                                                  var_calc_amount_energy_tax_g + \
            #                                                  var_calc_amount_durable_tax_g --deep
            # case.calc_amount_tax_claim = var_calc_amount_tax_claim = var_calc_amount_vat + var_calc_amount_energy_ode_tax --deep
            # Fixme: -- end --

            # deep
            var_calc_amount_energy_ode_tax = var_calc_amount_energy_tax_e + \
                                                             var_calc_amount_durable_tax_e + \
                                                             var_calc_amount_energy_tax_g + \
                                                             var_calc_amount_durable_tax_g

            case.calc_amount_tax_claim = var_calc_amount_vat + var_calc_amount_energy_ode_tax

            ## calculating from parsed values
            case.tax_return_lines_e = var_tax_return_lines_e = var_tax_return_lines_ee + var_tax_return_lines_de
            case.tax_return_lines_g = var_tax_return_lines_g = var_tax_return_lines_dg + var_tax_return_lines_eg
            case.tax_return_lines_energy = var_tax_return_lines_energy = var_tax_return_lines_e + var_tax_return_lines_g
            case.tax_return_lines_ode = var_tax_return_lines_ode = var_tax_return_lines_de + var_tax_return_lines_dg
            case.tax_return_lines_energy_ode = var_tax_return_energy_lines_ode = var_tax_return_lines_dg + \
                                                                           var_tax_return_lines_de + \
                                                                           var_tax_return_lines_eg + \
                                                                           var_tax_return_lines_ee

            ## calculate partial payments including costs
            part_paid = var_amount_payment_lines - var_amount_cost_lines
            case.amount_payment_cum = part_paid if part_paid <= 0 else 0

            if var_orig_nett_tax_total > 0 and part_paid >= 0:
                part = part_paid / var_orig_nett_tax_total
                part = part if part <= 1 else 1
            else:
                part = 0

            case.amount_nett_cum = var_orig_amount_nett * part
            case.amount_energy_tax_e_cum = var_amount_energy_tax_e_cum = var_orig_energy_tax_e * (
                    1 - part) - var_tax_return_lines_ee
            case.amount_durable_tax_e_cum = var_amount_durable_tax_e_cum = var_orig_durable_tax_e * (
                    1 - part) - var_tax_return_lines_de
            case.amount_energy_tax_g_cum = var_amount_energy_tax_g_cum = var_orig_energy_tax_g * (
                    1 - part) - var_tax_return_lines_eg
            case.amount_durable_tax_g_cum = var_amount_durable_tax_g_cum = var_orig_durable_tax_g * (
                    1 - part) - var_tax_return_lines_dg
            case.amount_energy_tax_cum = var_amount_energy_tax_cum = \
                                                    var_amount_energy_tax_e_cum + \
                                                    var_amount_durable_tax_e_cum + \
                                                    var_amount_energy_tax_g_cum + \
                                                    var_amount_durable_tax_g_cum
            case.amount_vat_cum = var_amount_vat_cum = \
                                                    var_orig_vat * (1 - part) - var_tax_return_lines_vat
            case.amount_tax_cum = var_amount_tax_cum = \
                                                    var_amount_vat_cum + var_amount_energy_tax_cum
            case.nett_tax_total_cum = var_orig_nett_tax_total + var_amount_tax_cum
            case.grand_total_cum = var_orig_nett_tax_total + var_amount_cost_lines - var_amount_payment_lines
            ## todo gepruts



    @api.depends('claim_line.due_date')
    def _compute_last_date(self):
        self.ensure_one()
        last_date = []
        for line in self.claim_line:
            last_date.append(line.due_date)
            self.last_line_date = max(last_date) if len(last_date) > 0 else False


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
    claim_date = fields.Date(
        string=_("Batch Date"),
        required=True,
        translate=False,
        readonly=False,
    )
    last_line_date = fields.Date(
        string='Last Line Date',
        store=True,
        readonly=True,
        compute='_compute_last_date'
    )
    claim_line = fields.One2many(
        'claim.line',
        'claim_id',
        string=_("Claim Line"),
        required=False,
        translate=False,
        readonly=False,
        copy=True
    )
    cost_line = fields.One2many(
        'cost.line',
        'claim_id',
        string=_("Cost Lines"),
        required=False,
        translate=False,
        readonly=False,
        copy=True,
        track_visibility='onchange',

    )
    tax_return_line = fields.One2many(
        'tax.return.line',
        'claim_id',
        string=_("Tax Return Line"),
        required=False,
        translate=False,
        readonly=False,
        copy=True,
        track_visibility = 'onchange',
    )
    payment_line = fields.One2many(
        'payment.line',
        'claim_id',
        string=_("Payment Line"),
        required=False,
        translate=False,
        readonly=False,
        copy=True,
        track_visibility='onchange',
    )
    zpartner = fields.Char(
        string=_("Debtor"),
        required=False,
        translate=False,
        readonly=False,
        size=64,
    )
    partnersrt = fields.Selection([
            ('CM','Consument'),
            ('KZM','Kein Zakelijk'),
        ],
        string='Debtor Type',
        required=False,
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
        #readonly=True,
        default=False,
        copy=False,
        help="It indicates that the tax return has been sent.",
        track_visibility = 'onchange',
        )
    bankruptcy = fields.Boolean(
        string=_("Faillissement"),
        # readonly=True,
        default=False,
        copy=False,
        help="It indicates that the debtor is in bankruptcy.",
        track_visibility='onchange',
    )
    wsnp = fields.Boolean(
        string=_("WSNP"),
        # readonly=True,
        default=False,
        copy=False,
        help="It indicates that the debtor is in WSNP.",
        track_visibility='onchange',
    )
    sued = fields.Boolean(
        string=_("Dagvaarding"),
        # readonly=True,
        default=False,
        copy=False,
        help="It indicates that the debtor has been sued.",
        track_visibility='onchange',
    )
    discharge = fields.Boolean(
        string=_("Finale Kwijting"),
        # readonly=True,
        default=False,
        copy=False,
        help="It indicates that agreement with the debtor has been reached with discharge.",
        track_visibility='onchange',
    )
    comment = fields.Text('Additional Information'
        )
    orig_amount_nett = fields.Float(
        string='Original Nett Claim Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_tax = fields.Float(
        string='Original Tax Amount',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_vat = fields.Float(
        string='Original VAT Amount',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_energy_tax_e = fields.Float(
        string='Original Energy Tax E',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_energy_tax_g = fields.Float(
        string='Original Energy Tax G',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_durable_tax_e = fields.Float(
        string='Original Durable Tax E',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_durable_tax_g = fields.Float(
        string='Original Durable Tax G',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_e_tax = fields.Float(
        string='Original Energy/ODE Tax E',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_g_tax = fields.Float(
        string='Original Energy/ODE Tax G',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_energy_tax = fields.Float(
        string='Original Energy Tax',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_ode_tax = fields.Float(
        string='Original ODE Tax',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_energy_ode_tax = fields.Float(
        string='Original Energy & ODE Tax',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_nett_tax_total = fields.Float(
        string='Original Nett plus Tax Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    orig_amount_total = fields.Float(
        string='Original Claim Total in DUT',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    total_claim_incl_cost = fields.Float(
        string='Total incl. Cost',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    total_claim_minus_payments = fields.Float(
        string='Balance',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    ###todo

    calc_amount_tax_claim = fields.Float(
        string='Tax Claim Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    calc_amount_vat = fields.Float(
        string='VAT Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    calc_amount_energy_tax_e = fields.Float(
        string='Energy Tax E Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    calc_amount_energy_tax_g = fields.Float(
        string='Energy Tax G Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    calc_amount_durable_tax_e = fields.Float(
        string='Durable Tax E Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    calc_amount_durable_tax_g = fields.Float(
        string='Durable Tax G Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    calc_amount_energy_tax = fields.Float(
        string='Energy Tax Calc',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    ##todo
    amount_cost_lines = fields.Float(
        string='Collection Cost',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_payment_lines = fields.Float(
        string='Payment',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_total = fields.Float(
        string='Total Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_ee = fields.Float(
        string='EE Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_de = fields.Float(
        string='DE Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_eg = fields.Float(
        string='EG Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_dg = fields.Float(
        string='DG Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_e = fields.Float(
        string='Electricity Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_g = fields.Float(
        string='Gas Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_energy = fields.Float(
        string='Energy Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_ode = fields.Float(
        string='Durable Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_energy_ode = fields.Float(
        string='Energy Total Tax Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_return_lines_vat = fields.Float(
        string='VAT Returned',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    ##todo
    amount_nett_cum = fields.Float(
        string='Nett Claim Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_tax_cum = fields.Float(
        string='Current Tax Claim',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_vat_cum = fields.Float(
        string='VAT Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_energy_tax_e_cum = fields.Float(
        string='Energy Tax E Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_energy_tax_g_cum = fields.Float(
        string='Energy Tax G Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_durable_tax_e_cum = fields.Float(
        string='Durable Tax E Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_durable_tax_g_cum = fields.Float(
        string='Durable Tax G Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_energy_tax_cum = fields.Float(
        string='Energy Tax Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_total_cum = fields.Float(
        string='Claim Original Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    nett_tax_total_cum = fields.Float(
        string='Nett plus Tax Total Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    grand_total_cum = fields.Float(
        string='Claim Grand Total',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_cost_cum = fields.Float(
        string='Collection Cost Cum',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount',
        track_visibility='always',
    )
    amount_payment_cum = fields.Float(
        string='Balance Payments/Costs',
        digits=dp.get_precision('claim'),
        store=True,
        readonly=True,
        compute='_compute_amount',
        track_visibility='always',
    )

    # @Job
    @api.model
    def generate_tax_lines_from_claim(self, declaration):
        context = self._context
        cutoff_type = context.get('cutoff', False)
        for claim in self:
            if cutoff_type == 'last_line':
                claim.make_tax_line_from_claim(declaration)
            else:
                claim.make_tax_line_from_claim_lines(declaration)


    def make_tax_line_from_claim(self, declaration):
        self.ensure_one()
        if abs(self.amount_tax_cum) < 0.01:
            return
        vals = {
            'claim_id': self.id,
            'declaration_id': declaration.id,
            'date_tax_request': declaration.date_tax_request,
            'energy_tax_e_return': self.amount_energy_tax_e_cum,
            'energy_tax_g_return': self.amount_energy_tax_g_cum,
            'vat_return': self.amount_vat_cum,
            'durable_tax_e_return': self.amount_durable_tax_e_cum,
            'durable_tax_g_return': self.amount_durable_tax_g_cum,
            'docsoort': 'TR' if self.amount_tax_cum >= 0 else 'TD'
        }
        return self.env['tax.return.line'].create(vals)


    def make_tax_line_from_claim_lines(self, declaration):
        self.ensure_one()
        if self.last_line_date <= declaration.to_invoice_date:
            self.make_tax_line_from_claim(declaration)
        else:
            # claim_lines = self.env['claim.line'].search(
            #     [('due_date', '<=', declaration.to_invoice_date), ('claim_id', '=', self.id)])
            vals = self.compute_amount()
            vals['declaration_id'] = declaration.id
            vals['date_tax_request'] = declaration.date_tax_request
            if abs(vals['energy_tax_e_return']) < 0.01 and abs(vals['energy_tax_g_return']) < 0.01 \
                and abs(vals['vat_return']) < 0.01 and abs(vals['durable_tax_e_return']) < 0.01 \
                and abs(vals['durable_tax_g_return']) < 0.01:
                return
            self.env['tax.return.line'].create(vals)
        return True

    def compute_amount(self):
        vals = {
            'claim_id': self.id,
            'energy_tax_e_return': self.amount_energy_tax_e_cum,
            'energy_tax_g_return': self.amount_energy_tax_g_cum,
            'vat_return': self.amount_vat_cum,
            'durable_tax_e_return': self.amount_durable_tax_e_cum,
            'durable_tax_g_return': self.amount_durable_tax_g_cum,
            'docsoort': 'TR' if self.amount_tax_cum >= 0 else 'TD'
        }
        return vals
