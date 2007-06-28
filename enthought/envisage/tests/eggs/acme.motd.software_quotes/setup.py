# Major package imports.
from setuptools import setup, find_packages

setup(
    name                 = 'acme.motd.software_quotes',
    version              = '0.1a1',
    author               = 'Enthought, Inc',
    author_email         = 'info@enthought.com',
    license              = 'BSD',
    zip_safe             = True,
    packages             = find_packages(),
    include_package_data = True,

    namespace_packages   = [
        'acme',
        'acme.motd',
        'acme.motd.software_quotes'
    ],

    install_requires     = [
        'acme.motd'
    ],


    entry_points = """

    [acme.motd.messages]
    meyer       = acme.motd.software_quotes.messages:meyer
    dijkstra    = acme.motd.software_quotes.messages:dijkstra
    fuller      = acme.motd.software_quotes.messages:fuller
    gilb        = acme.motd.software_quotes.messages:gilb
    norman      = acme.motd.software_quotes.messages:norman
    einstein    = acme.motd.software_quotes.messages:einstein
    fowler      = acme.motd.software_quotes.messages:fowler
    hendrickson = acme.motd.software_quotes.messages:hendrickson
    jeffries    = acme.motd.software_quotes.messages:jeffries
    tuft        = acme.motd.software_quotes.messages:tuft

    """
    
)
