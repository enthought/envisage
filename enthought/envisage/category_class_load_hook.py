""" A class load hook that imports and adds a category. """


# Enthought library imports.
from enthought.traits.api import Instance, Str

# Local imports.
from class_load_hook import ClassLoadHook
from i_import_manager import IImportManager
from import_manager import ImportManager


class CategoryClassLoadHook(ClassLoadHook):
    """ A class load hook that imports and adds a category. """

    #### 'CategoryImporter' interface #########################################

    # The possibly dotted path to the category class that we want to add when
    # the class is loaded.
    category_class_name = Str

    # The import manager used to import the category class.
    import_manager = Instance(IImportManager, ImportManager())

    ###########################################################################
    # 'ClassLoadHook' interface.
    ###########################################################################

    def on_class_loaded(self, cls):
        """ This method is called when the class is loaded. """

        category = self.import_manager.import_symbol(self.category_class_name)
        cls.add_trait_category(category)

        return

#### EOF ######################################################################
