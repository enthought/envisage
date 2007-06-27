# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.workbench',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = ['acme'],
    install_requires     = ['enthought.envisage3.ui.workbench'],

    entry_points = """

    [enthought.envisage3.ui.workbench.views]
    black  = acme.workbench.view.api:BlackView
    blue   = acme.workbench.view.api:BlueView
    green  = acme.workbench.view.api:GreenView
    red    = acme.workbench.view.api:RedView
    yellow = acme.workbench.view.api:YellowView

    [enthought.envisage3.ui.workbench.perspectives]
    foo = acme.workbench.perspective.api:FooPerspective
    bar = acme.workbench.perspective.api:BarPerspective

    """
)
