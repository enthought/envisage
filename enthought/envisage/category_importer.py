""" A class load hook that imports and adds a category! """


# Standard library imports.
import sys

# Enthought library imports.
from enthought.traits.api import Str

# Local imports.
from class_load_hook import ClassLoadHook
from import_manager import ImportManager


class CategoryImporter(ClassLoadHook):
    """ A class load hook that imports and adds a category! """

    #### 'CategoryImporter' *class* interface #################################
    
    # fixme: We would really like to use the application's import manager, but
    # we don't really want to have to pass the application into every hook!
    import_manager = ImportManager()

    #### 'CategoryImporter' interface #########################################

    # The possibly dotted path to the category class that we want to add when
    # the class is loaded.
    category_class_name = Str

    ###########################################################################
    # 'ClassLoadHook' interface.
    ###########################################################################

    def on_class_loaded(self, cls):
        """ This method is called when the class is loaded. """

        category = self.import_manager.import_symbol(self.category_class_name)
        cls.add_trait_category(category)

        return

#### EOF ######################################################################
