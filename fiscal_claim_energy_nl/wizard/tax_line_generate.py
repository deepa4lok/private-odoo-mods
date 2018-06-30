# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2004-2018 Willem Hulshof https://www.magnus.nl
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

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.queue_job.job import job, related_action
from odoo.addons.queue_job.exception import FailedJobError
from unidecode import unidecode


class ClaimTaxLineGen(models.TransientModel):
    _name = "claim.tax.line.gen"
    _description = "Claim Tax Lines Generate"

    declaration = fields.Many2one('tax.declaration')
    job_queue = fields.Boolean('Process via Job Queue', default=False)
    chunk_size = fields.Integer('Chunk Size Job Queue', default=50)
    execution_datetime = fields.Datetime('Job Execution not before', default=fields.Datetime.now())



    @api.multi
    def generate_tax_lines(self):
        context = self._context

        declaration_ids = context.get('active_ids', [])
        declarations = self.env['tax.declaration'].search([('id','in', declaration_ids)])
        ctx = context.copy()
        ctx['chunk_size'] = self.chunk_size
        ctx['job_queue'] = self.job_queue
        ctx['execution_datetime'] = self.execution_datetime
        for decl in declarations:
            if decl.cutoff == 'line_date':
                sql = ("SELECT claim_id from claim_line"
                       " WHERE due_date <= %s"
                       " GROUP BY claim_id")
                self.env.cr.execute(sql, (decl.to_invoice_date,))
                claim_ids = self.env.cr.fetchall()
                claims = self.env['claim'].search([('id','in', claim_ids),
                                                   ('claim_date','>=', decl.from_batch_date),
                                                   ('claim_date','<=', decl.to_batch_date),
                                                   ('amount_tax_cum', '!=', 0)])
                ctx['cutoff'] = 'line_date'
            else:
                claims = self.env['claim'].search([('last_line_date','<=', decl.to_invoice_date),
                                                   ('claim_date','>=', decl.from_batch_date),
                                                   ('claim_date','<=', decl.to_batch_date),
                                                   ('amount_tax_cum','!=', 0)])
                ctx['cutoff'] = 'last_line'
            claims.with_context(ctx).generate_tax_lines_from_claim(decl)
        return True



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
