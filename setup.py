from setuptools import setup, find_packages


# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
TRAITS = etsdep('enthought.traits', '3.0.0b1')
UTIL = etsdep('enthought.util', '3.0.0a1')


setup(
    author = "Martin Chilvers",
    author_email = "info@enthought.com",
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        'http://code.enthought.com/enstaller/eggs/source/unstable',
        ],
    description = "Envisage - An Extensible Application Framework",
    extras_require = {
        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            ],
        },
    ext_modules = [],
    include_package_data = True,
    install_requires = [
        TRAITS,
        UTIL,
        ],
    license = "BSD",
    name = "enthought.envisage",
    namespace_packages   = [
        "enthought",
        "enthought.envisage"
        ],
    packages = find_packages(),
    url = "http://code.enthought.com/envisage",
    version = "3.0.0a2",
    zip_safe = False,
    )
