# -*- coding: utf-8 -*-
# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# Copyright 2017 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from odoo import _, api, SUPERUSER_ID

_logger = logging.getLogger(__name__)



def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        # calculating all last_line_date fields
        claims = env['claim'].search([
            (1, '=', 1)
        ])
        _logger.info("Calculating %d claims", len(claims))
        for claim in claims:
            claim._compute_last_date()

