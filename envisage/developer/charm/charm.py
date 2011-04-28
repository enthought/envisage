""" Charm - the model for a simple Python IDE. """


# Enthought library imports.
from envisage.developer.api import CodeBrowser, Module
from traits.api import Event, HasTraits, Instance, Str


class Charm(HasTraits):
    """ Charm - the model for a simple Python IDE. """

    #### 'Charm' interface ####################################################

    # The code browser.
    code_browser = Instance(CodeBrowser)

    # The filename of the code database.
    filename = Str('code_database.pickle')

    # The current module.
    module = Instance(Module)

    #### Events ####

    # Fired when a module is about to be parsed.
    parsing_module = Event

    # Fired when a module has been parsed.
    parsed_module = Event

    ###########################################################################
    # 'Charm' interface.
    ###########################################################################

    #### Trait initializers ###################################################

    def _code_browser_default(self):
        """ Trait initializer. """

        code_browser = CodeBrowser(filename=self.filename)
        self._setup_code_browser(code_browser)

        return code_browser

    #### Methods ##############################################################

    def load(self):
        """ Loads the code database. """

        self.code_browser.load()

        return

    def save(self):
        """ Saves the code database. """

        self.code_browser.save()

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _setup_code_browser(self, code_browser):
        """ Adds trait change listeners to a code browser. """

        code_browser.on_trait_change(self._on_parsing_module, 'parsing_module')
        code_browser.on_trait_change(self._on_parsed_module, 'parsed_module')

        return

    def _tear_down_code_browser(self, code_browser):
        """ Removes trait change listeners from a code browser. """

        code_browser.on_trait_change(
            self._on_parsing_module, 'parsing_module', remove=True
        )

        code_browser.on_trait_change(
            self._on_parsed_module, 'parsed_module', remove=True
        )

        return

    #### Trait change handlers ################################################

    def _code_browser_changed(self, old, new):
        """ Static trait change handler. """

        if old is not None:
            self._tear_down_code_browser(old)

        if new is not None:
            self._setup_code_browser(new)

        return

    def _filename_changed(self, old, new):
        """ Static trait change handler. """

        self.code_browser.filename = new

        return

    def _on_parsing_module(self, event):
        """ Dysnamic trait change handler. """

        self.parsing_module = event

        return

    def _on_parsed_module(self, event):
        """ Dysnamic trait change handler. """

        self.parsed_module = event

        return

#### EOF ######################################################################
