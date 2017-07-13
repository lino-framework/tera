# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The default :attr:`custom_layouts_module
<lino.core.site.Site.custom_layouts_module>` for Lino Tera.

"""

from lino.api import rt
rt.models.accounts.Accounts.column_names = "\
ref name purchases_allowed group *"

rt.models.accounts.Accounts.detail_layout = """
ref:10 name
group type id default_amount:10 vat_column
needs_partner clearable purchases_allowed  needs_ana ana_account
ledger.MovementsByAccount
"""


rt.models.system.SiteConfigs.detail_layout = """
site_company next_partner_id:10
default_build_method simulate_today
clients_account   sales_account
suppliers_account purchases_account tax_offices_account
site_calendar default_event_type #pupil_guestrole
max_auto_events hide_events_before
"""


# rt.models.vat.ItemsByInvoice.column_names = "account title ana_account vat_class total_base total_vat total_incl"

# select Belgian VAT declaration layout
# from lino_xl.lib.declarations import be
