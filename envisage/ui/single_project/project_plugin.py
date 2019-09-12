# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
""" The Envisage single project plugin. """

# Standard library imports
import logging

# Enthought library imports.
from envisage.api import ExtensionPoint, Plugin, ServiceOffer
from envisage.ui.single_project.api import FactoryDefinition
from pyface.action.api import MenuManager
from pyface.workbench.api import Perspective
from traits.api import Callable, List

# Local imports.
from .model_service import ModelService
from .project_action_set import ProjectActionSet
from .services import IPROJECT_MODEL, IPROJECT_UI
from .ui_service_factory import UIServiceFactory

# This module's package.
PKG = '.'.join(__name__.split('.')[:-1])

# Setup a logger for this module.
logger = logging.getLogger(__name__)

###############################################################################
# `ProjectPerspective` class.
###############################################################################
class ProjectPerspective(Perspective):
    """
    A default perspective for the single_project plugin.

    """

    # The perspective's name.
    name = 'Project'

    # Should this perspective be enabled or not?
    enabled = True

    # Should the editor area be shown in this perspective?
    show_editor_area = True

    # The contents of the perspective.
    # TODO: Setup the PerspectiveItems based on the areas in our perspective.
    #contents = []

##############################################################################
# 'ProjectPlugin' class.
##############################################################################
class ProjectPlugin(Plugin):
    """
    The single-project plugin.

    """

    # The Ids of the extension points that this plugin offers.
    ACTION_SETS       = 'envisage.ui.workbench.action_sets'
    FACTORY_DEFINITIONS = 'envisage.ui.single_project.factory_definitions'
    UI_SERVICE_FACTORY = 'envisage.ui.single_project.ui_service_factory'

    # The Ids of the extension points that this plugin contributes to.
    PERSPECTIVES = 'envisage.ui.workbench.perspectives'
    PREFERENCES = 'envisage.preferences'
    PREFERENCES_PAGES = 'envisage.ui.workbench.preferences_pages'
    SERVICE_OFFERS = 'envisage.service_offers'
    VIEWS = 'envisage.ui.workbench.views'

    #### 'IPlugin' interface ##################################################

    # The plugin's unique identifier.
    id = 'envisage.ui.single_project'

    # The plugin's name (suitable for displaying to the user).
    name = 'Single Project'

    #### Extension points offered by this plugin ##############################

    # Factory definitions.
    factory_definitions = ExtensionPoint(
        List(Callable), id=FACTORY_DEFINITIONS, desc="""

        A project factory definition.

        An instance of the specified class is used to open and/or create new
        projects.

        The extension with the highest priority wins!  In the event of a tie,
        the first instance wins.

        """
    )

    # Ui service factories.
    ui_service_factory = ExtensionPoint(
        List(Callable), id=UI_SERVICE_FACTORY, desc="""

        A ui service factory definition.

        """
    )

    #### Contributions to extension points made by this plugin ################

    # Action sets.
    action_sets = List(contributes_to=ACTION_SETS)

    def _action_sets_default(self):
        """
        Default project actions.

        """

        return [ProjectActionSet]

    # Factory definitions.
    my_factory_definitions = List(contributes_to=FACTORY_DEFINITIONS)

    def _my_factory_definitions_default(self):
        """
        Default factory definition.

        """

        factory_definition = FactoryDefinition(
            class_name = PKG + '.project_factory.ProjectFactory',
            priority = 0,
        )

        return [factory_definition]

    # Perspectives.
    perspectives = List(contributes_to=PERSPECTIVES)

    def _perspectives_default(self):
        """
        Default project perspective.

        """

        return [ProjectPerspective]

    # Service offers.
    service_offers = List(contributes_to=SERVICE_OFFERS)

    def _service_offers_default(self):
        """
        Our service contributions.

        """

        model_service = ServiceOffer(
            protocol = IPROJECT_MODEL,
            factory  = self._create_model_service
        )

        ui_service = ServiceOffer(
            protocol = IPROJECT_UI,
            factory  = self._create_ui_service
        )

        # FIXME: Eventually we will register the services here intead
        # of in the plugin's start() method.
        #return [model_service, ui_service]
        return []

    # Ui service factories.
    my_ui_service_factory = List(contributes_to=UI_SERVICE_FACTORY)

    def _my_ui_service_factory_default(self):
        """
        Default ui service factory.

        """

        ui_service_factory = UIServiceFactory(
            class_name = PKG + '.ui_service_factory.UIServiceFactory',
            priority = 0,
        )

        return [ui_service_factory]

    # Preferences.
    my_preferences = List(contributes_to=PREFERENCES)

    def _my_preferences_default(self):
        """
        Default preferences.

        """
        return ['pkgfile://%s/preferences.ini' % PKG]

    # Preference pages.
    my_preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    def _my_preferences_pages_default(self):
        """
        Default preference page.

        """

        from .default_path_preference_page import DefaultPathPreferencePage

        return [DefaultPathPreferencePage]

    # Views.
    views = List(contributes_to=VIEWS)

    def _views_default(self):
        """
        Add our project views.

        """

        return [self._project_view_factory]

    ### protected interface ##################################################

    def start(self):
        """
        Starts the plugin.

        Overridden here to start up our services and load the project
        that was open when we were last shut-down.

        """

        super(ProjectPlugin, self).start()

        # FIXME: We eventually won't have to explicitly register the
        # services ourselves, since we contribute them as service offers
        # so they are instantiated when they are invoked, but since they are
        # not used anywhere else yet, I had to use this same old approach
        # just to test and make sure they were working correctly.
        # Create and register the model service we offer
        model_service = self._create_model_service()
        self.application.register_service(IPROJECT_MODEL, model_service)

        # Create and register the ui service we offer
        ui_service = self._create_ui_service(model_service)
        self.application.register_service(IPROJECT_UI, ui_service)

        # Set up any listeners interested in the current project selection
        # FIXME: Register the selection listeners for the current project selection.
        #self._register_selection_listeners(model_service)

        return

    ######################################################################
    # Private methods.
    def _project_view_factory(self, window, **traits):
        """
        Factory method for project views.

        """
        from pyface.workbench.traits_ui_view import \
                TraitsUIView
        from envisage.ui.single_project.api import \
                            ProjectView

        project_view = ProjectView(application=window.application)
        tui_project_view = TraitsUIView(obj=project_view,
                                       id='envisage.ui.single_project.view.project_view.ProjectView',
                                       name='Project View',
                                       window=window,
                                       position='left',
                                       **traits
                                       )
        return tui_project_view

    def _create_model_service(self):
        """
        Creates a model service for this plugin.

        """

        # Determine which contributed project factory to use.
        factory = self._get_contributed_project_factory()

        # Make sure the factory has a reference to our Envisage application.
        factory.application = self.application

        # Create the project service instance.
        result = ModelService(self.application, factory)

        return result


    def _create_ui_service(self, model_service):
        """
        Creates a UI service for this plugin.

        """

        # Create the menu manager representing the context menu we show when
        # nothing is selected in the project view.
        menu_manager = self._get_no_selection_context_menu_manager()

        # Get the UI service factory.
        ui_service_factory = self._get_contributed_ui_service_factory()

        # Create the ui service instance
        ui_service = ui_service_factory.create_ui_service(model_service,
            menu_manager)

        return ui_service


    def _get_contributed_project_factory(self):
        """
        Retrieves the instance of the project factory to use with this
        plugin.

        The instance is generated from the contributed factory definition
        that was the first one with the highest priority.

        """

        # Retrieve all the factory definition contributions
        extensions = self.application.get_extensions('envisage.ui.single_project.factory_definitions')

        # Find the winning contribution
        definition = None
        for extension in extensions:
            if not definition or extension.priority > definition.priority:
                definition = extension

        # Create an instance of the winning project factory
        logger.info("Using ProjectFactory [%s]", definition.class_name)
        klass = self.application.import_symbol(definition.class_name)
        factory = klass()

        return factory


    def _get_contributed_ui_service_factory(self):
        """
        Retrieves the instance of the UiService factory to use with this
        plugin.

        The instance is generated from the contributed factory definition
        that was the first one with the highest priority.

        """

        # Retrieve all the factory definition contributions
        extensions = self.get_extensions('envisage.ui.single_project.ui_service_factory')

        # Find the winning contribution
        definition = None
        for extension in extensions:
            if not definition or extension.priority > definition.priority:
                definition = extension

        # Create an instance of the winning factory
        logger.info("Using UiService Factory [%s]", definition.class_name)
        class_name = definition.class_name
        klass = self.application.import_symbol(class_name)
        factory = klass()

        return factory


    def _get_no_selection_context_menu_manager(self):
        """
        Generates a menu manager representing the context menu shown when
        nothing is selected within the project view.  That is, when the
        user right clicks on any empty space within our associated UI.

        """

        # Retrieve all contributions for the no-selection context menu.
        extensions = self.get_extensions(ProjectActionSet)

        # Populate a menu manager from the extensions.
        menu_manager = MenuManager()
        if len(extensions) > 0:
            action_set_manager = ActionSetManager(action_sets=extensions)
            menu_builder = DefaultMenuBuilder(application=self.application)
            menu_builder.initialize_menu_manager(menu_manager,
                action_set_manager, NO_SELECTION_MENU_ID)

        return menu_manager


    def _register_selection_listeners(self, model_service):
        """
        Registers any extension-requested listeners on the project
        selection.

        """

        for sps in self.get_extensions(SyncProjectSelection):
            object = self.application.lookup_application_object(sps.uol)
            if object is not None:
                name = sps.name
                self._register_selection_handler(object, name, model_service)
            else:
                logger.error('Could not resolve the SyncProjectSelection ' + \
                    'UOL: "%s"', sps.uol )

        return


    def _register_selection_handler(self, object, name, model_service):
        """
        Creates a handler and registers it.

        """

        def handler():
            # The key to this method is to realize that our goal is to
            # make it as easy as possible to create recipients for
            # notification.  Using traits as the recipients makes
            # creation very simple because we can rely on the type
            # knowledge within that trait to ensure only valid values
            # get assigned to the recipient.  That is the recipient
            # doesn't need to do anything complex to validate the
            # values they get assigned.  This method also works if the
            # recipient isn't a trait, but in that case, they will
            # have to handle multiple selection of the project
            # bindings.
            #
            # First, try to provide the recipient with a multiple
            # selection type value i.e. a list of bindings.
            try:
                setattr(object, name, model_service.selection)
                return
            except:
                pass

            # If that didn't work, remove the binding wrappers and try
            # notification of the resulting list.
            selection = [s.obj for s in model_service.selection]
            try:
                setattr(object, name, selection)
                return
            except:
                pass

            # If that didn't work, and only a single item is selected,
            # then try to provide that item to the recipient.
            if len(selection) == 1:
                try:
                    setattr(object, name, selection[0])
                    return
                except:
                    pass

            # The recipient must not be accepting the type of the
            # current selection, so let's clear its current selection
            # instead.  If this fails, then something has gone wrong
            # with the declaration of the recipient.
            try:
                setattr(object, name, None)
            except:
                logger.debug('Error informing object [%s] of project '
                    'selection change via attribute [%s]', object, name)

        model_service.on_trait_change(handler, 'selection')
        model_service.on_trait_change(handler, 'selection_items')

        return

### EOF ######################################################################
