# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The default :attr:`custom_layouts_module
<lino.core.site.Site.custom_layouts_module>` for Lino Tera.

"""

from lino.api import rt
rt.actors.accounts.Accounts.column_names = "\
ref name purchases_allowed group *"

rt.actors.accounts.Accounts.detail_layout = """
ref:10 name
group type id default_amount:10
needs_partner:30 clearable:30 purchases_allowed 
ledger.MovementsByAccount
"""

# select Belgian VAT declaration layout
# from lino_xl.lib.declarations import be
