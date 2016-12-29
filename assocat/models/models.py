# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
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
 
from openerp import models, fields, api, tools, _
#from openerp.osv import fields as fields_old
#import openerp.addons.decimal_precision as dp

class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = ['account.analytic.line',]
    _description = 'Kostenplaatsboeking'

    poppetje = fields.Char( required=True, string='POP',inverse='_inverse_poppetje',)
    

    @api.depends('poppetje',)
    def _inverse_poppetje():
        self.poppetje = False
    

class Lidje(models.Model):
    _name = 'lidje'
    _inherits = {'account.analytic.account' : 'kots', }
    _description = 'lidje'

    date = fields.Date( required=True, string='datum',compute='_compute_date',)
    name = fields.Char( size=64, required=True, string='Omschrijving',)
    

    @api.depends('date',)
    def _compute_date():
        self.date = False
    
