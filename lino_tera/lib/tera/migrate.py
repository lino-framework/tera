# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
This is an example of how the application developer can provide
automatic data migrations.

This module is used because a :ref:`tera` Site has
:attr:`migration_class <lino.core.site.Site.migration_class>` set to
``"lino_tera.lib.tera.migrate.Migrator"``.
"""

from decimal import Decimal
from django.conf import settings
from lino.api import dd, rt
from lino.utils.dpy import Migrator, override
from lino.utils.dpy import create_mti_child


def noop(*args):
    return None


class Migrator(Migrator):
    "The standard migrator for :ref:`tera`."

    def migrate_from_18_8_0(self, globals_dict):
        """
        min_asset and number_of_events now in Tarif instead Product

        """

        bv2kw = globals_dict['bv2kw']
        products_Product = rt.models.products.Product
        
        @override(globals_dict)
        def create_products_product(id, name, description, cat_id, delivery_unit, vat_class, number_of_events, min_asset, sales_account_id, sales_price):
        #    if delivery_unit: delivery_unit = settings.SITE.models.products.DeliveryUnits.get_by_value(delivery_unit)
        #    if vat_class: vat_class = settings.SITE.models.vat.VatClasses.get_by_value(vat_class)
            if sales_price is not None: sales_price = Decimal(sales_price)
            kw = dict()
            kw.update(id=id)
            if name is not None: kw.update(bv2kw('name',name))
            if description is not None: kw.update(bv2kw('description',description))
            kw.update(cat_id=cat_id)
            kw.update(delivery_unit=delivery_unit)
            kw.update(vat_class=vat_class)
            #kw.update(number_of_events=number_of_events)
            #kw.update(min_asset=min_asset)
            kw.update(sales_account_id=sales_account_id)
            kw.update(sales_price=sales_price)
            return products_Product(**kw)

        return '18.11.0'

