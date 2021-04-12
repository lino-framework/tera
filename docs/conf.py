# -*- coding: utf-8 -*-
from lino.sphinxcontrib import configure
configure(globals())
extensions += ['lino.sphinxcontrib.logo']
# from atelier.sphinxconf import interproject
# interproject.configure(globals(), 'atelier')

project = "Lino Tera"
copyright = '2014-2021 Rumma & Ko Ltd'
html_title = "Lino Tera"
html_context.update(public_url='https://tera.lino-framework.org')
# suppress_warnings = ['image.nonlocal_uri']
