# (C) Copyright 2007-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# Major package imports.
from setuptools import find_packages, setup

setup(
    name="acme-bad",
    version="0.1a1",
    author="Enthought, Inc",
    author_email="info@enthought.com",
    license="BSD",
    zip_safe=True,
    packages=find_packages(include="acme_bad*"),
    include_package_data=True,
    install_requires=["acme-foo"],
    entry_points="""

    [envisage.plugins]
    acme.bad = acme_bad.bad_plugin:BadPlugin

    """,
)
