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

{
    'name': 'Fiscal Claim Energy NL',
    'version': '8.0.1.0.0',
    'author': 'hulshof',
    'maintainer': 'False',
    'website': 'False',
    'license': '',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml # noqa
    # for the full list
    'category': 'Others',    'summary': 'This module processes the fiscal part of session claim batches for the energy industry in NL',
    'description': """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=======================
Fiscal Claim Energy NL
=======================

This module was written to handle the tax returns of cession claims portfolios in the energy industry in the netherlands
and allows you to import batches of claims assigned to assignee (or debt trader)

Installation
============

To install this module, you need to:

 start een empty Odoo server and install this module

Configuration
=============

To configure this module, you need to:

 * go to ...

Usage
=====

To use this module, you need to:

 * go to ...

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/{repo_id}/{branch}

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

For further information, please visit:

 * https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

 * ...

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/{project_repo}/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/{project_repo}/issues/new?body=module:%20{module_name}%0Aversion:%20{version}%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

Contributors
------------

* Firstname Lastname <email.address@example.org>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.

* Module exported by the Module Prototyper module for version 8.0.
* If you have any questions, please contact Savoir-faire Linux
(support@savoirfairelinux.com)
""",

    # any module necessary for this one to work correctly
    'depends': ['decimal_precision',
                'mail','mis_builder',
    ],
    'external_dependencies': {
        'python': [],
    },

    # always loaded
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'views/claim_view.xml',
            'views/ir_ui_menus.xml',
            'wizard/tax_line_generate.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],

    # used for Javascript Web CLient Testing with QUnit / PhantomJS
    # https://www.odoo.com/documentation/8.0/reference/javascript.html#testing-in-odoo-web-client  # noqa
    'js': [],
    'css': [],
    'qweb': [],

    'installable': True,
    "post_init_hook": "post_init_hook",
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    'auto_install': False,
    'application': True,
}
