import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from distutils.command.build import build as distbuild
from pkg_resources import require
from make_docs import HtmlBuild

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
APPTOOLS = etsdep('AppTools', '3.0.0b1')
ENTHOUGHTBASE = etsdep('EnthoughtBase', '3.0.0b1')
TRAITS = etsdep('Traits', '3.0.0b1')

def generate_docs():
    """If sphinx is installed, generate docs.
    """
    doc_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),'docs')
    dest_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        'build', 'docs')
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    try:
        require("Sphinx>=0.4.1")
            
        #log.info("Auto-generating documentation...")
        doc_src = doc_dir
        target = dest_dir
        try:
            build = HtmlBuild()
            build.start({
                'commit_message': None,
                'doc_source': doc_src,
                'preserve_temp': True,
                'subversion': False,
                'target': target,
                'verbose': True,
                'versioned': False,
                }, [])
            del build
        except:
            #log.error("The documentation generation failed.  Falling back to the zip file.")
            print "oops1"
    except: #DistributionNotFound:
        #log.error("Sphinx is not installed, so the documentation could not be generated.  Falling back to the zip file.")
        print "oops"

class my_develop(develop):
    def run(self):
        develop.run(self)
        print "\n############################ hello\n"
        generate_docs()

class my_build(distbuild):
    def run(self):
        distbuild.run(self)

        # Generate the documentation.
        generate_docs()

setup(
    author = "Martin Chilvers",
    author_email = "info@enthought.com",
    cmdclass = {
        'develop': my_develop,
        'build': my_build
        },
    dependency_links = [
        'http://code.enthought.com/enstaller/eggs/source',
        ],
    description = "Envisage - An Extensible Application Framework",
    entry_points = """
        [enthought.envisage.plugins]
        core = enthought.envisage.core_plugin:CorePlugin
        """,
    extras_require = {
        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            ],
        },
    ext_modules = [],
    include_package_data = True,
    install_requires = [
        APPTOOLS,
        ENTHOUGHTBASE,
        TRAITS,
        ],
    license = "BSD",
    name = "EnvisageCore",
    namespace_packages   = [
        "enthought",
        "enthought.envisage"
        ],
    packages = find_packages(),
    url = "http://code.enthought.com/envisage",
    version = "3.0.0b1",
    zip_safe = False,
    )

