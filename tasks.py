from lino.invlib.ns import ns
ns.setup_from_tasks(
    globals(), "lino_tera",
    languages="en de fr et".split(),
    tolerate_sphinx_warnings=False,
    blogref_url='http://luc.lino-framework.org',
    revision_control_system='git',
    locale_dir='lino_tera/lib/tera/locale',
)
