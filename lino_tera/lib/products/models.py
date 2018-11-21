# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

from lino_xl.lib.products.models import *
from lino.api import _


ProductTypes.clear()
add = ProductTypes.add_item
add('100', _("Fee"), 'default')
add('200', _("Payment"), 'payment')
add('300', _("Other"), 'other')



class ProductCat(ProductCat):
    class Meta(ProductCat.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'ProductCat')
        verbose_name = _("Fee category")
        verbose_name_plural = _("Fee categories")


class Product(Product):

    class Meta(Product.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'Product')
        verbose_name = _("Fee")
        verbose_name_plural = _("Fees")


class ProductDetail(dd.DetailLayout):

    main = "general courses sales"
    
    general = dd.Panel("""
    name id 
    product_type cat sales_price tariff
    # tariff__number_of_events:10 tariff__min_asset:10 tariff__max_asset:10
    vat_class sales_account delivery_unit
    description
    """, _("General"))

    courses = dd.Panel("""
    courses.EnrolmentsByFee
    courses.EnrolmentsByOption
    """, _("Enrolments"))

    sales = dd.Panel("""
    sales.InvoiceItemsByProduct
    """, _("Sales"))


Products.column_names = "id name sales_price sales_account cat *"
