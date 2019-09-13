# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
A service to enable UI interactions with the single project plugin.

"""

# Standard library imports.
import logging
import os
import shutil

# Enthought library imports
from apptools.preferences.api import bind_preference
from apptools.io.api import File
from apptools.naming.api import Context
from pyface.api import CANCEL, confirm, ConfirmationDialog, \
    DirectoryDialog, error, FileDialog, information, NO, OK, YES
from pyface.action.api import MenuManager
from pyface.timer.api import do_later, Timer
from traits.api import Any, Event, HasTraits, Instance, Int

# Local imports.
from .model_service import ModelService


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class UiService(HasTraits):
    """
    A service to enable UI interactions with the single project plugin.

    """

    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'UiService' interface ########################################

    # The manager of the default context menu
    default_context_menu_manager = Instance(MenuManager)

    # A reference to our plugin's model service.
    model_service = Instance(ModelService)

    # The project control (in our case a tree). This is created by the
    # project view.  Provided here so that sub-classes may access it.
    project_control = Any

    # Fired when a new project has been created.  The value should be the
    # project instance that was created.
    project_created = Event

    # A timer to implement automatic project saving.
    timer = Instance(Timer)

    # The interval (minutes)at which automatic saving should occur.
    autosave_interval = Int(5)

    ##########################################################################
    # 'object' interface.
    ##########################################################################

    #### operator methods ####################################################

    def __init__(self, model_service, menu_manager, **traits):
        """
        Constructor.

        Extended to require a reference to the plugin's model service to create
        an instance.

        """

        super(UiService, self).__init__(
            model_service = model_service,
            default_context_menu_manager = menu_manager,
            **traits
            )
        try:
            # Bind the autosave interval to the value specified in the
            # single project preferences
            p = self.model_service.preferences
            bind_preference(self, 'autosave_interval', 5, p)
        except:
            logger.exception('Failed to bind autosave_interval in [%s] to '
                             'preferences.' % self)

        return


    ##########################################################################
    # 'UiService' interface.
    ##########################################################################

    #### public interface ####################################################

    def close(self, event):
        """
        Close the current project.

        """

        # Ensure any current project is ready for this change.
        if self.is_current_project_saved(event.window.control):

            # If we have a current project, close it.
            current = self.model_service.project
            if current is not None:
                logger.debug("Closing Project [%s]", current.name)
                self.model_service.project = None

        return


    def create(self, event):
        """
        Create a new project.

        """
        # Ensure any current project is ready for this change.
        if self.is_current_project_saved(event.window.control):

            # Use the registered factory to create a new project
            project = self.model_service.factory.create()
            if project is not None:

                # Allow the user to customize the new project
                dialog = project.edit_traits(
                    parent = event.window.control,
                    # FIXME: Due to a bug in traits, using a wizard dialog
                    # causes all of the Instance traits on the object being
                    # edited to be replaced with new instances without any
                    # listeners on those traits being called.  Since we can't
                    # guarantee that our project's don't have Instance traits,
                    # we can't use the wizard dialog type.
                    #kind = 'wizard'
                    kind = 'livemodal'
                    )

                # If the user closed the dialog with an ok, make it the
                # current project.
                if dialog.result:
                    logger.debug("Created Project [%s]", project.name)
                    self.model_service.project = project
                    self.project_created = project

        return


    def display_default_context_menu(self, parent, event):
        """
        Display the default context menu for the plugin's ui.  This is the
        context menu used when neither a project nor the project's contents
        are right-clicked.

        """

        # Determine the current workbench window.  This should be safe since
        # we're only building a context menu when the user clicked on a
        # control that is contained in a window.
        workbench = self.model_service.application.get_service('envisage.ui.workbench.workbench.Workbench')
        window = workbench.active_window

        # Build our menu
        from envisage.workbench.action.action_controller import \
            ActionController
        menu = self.default_context_menu_manager.create_menu(parent,
            controller = ActionController(window=window))

        # Popup the menu (if an action is selected it will be performed
        # before before 'PopupMenu' returns).
        if menu.GetMenuItemCount() > 0:
            menu.show(event.x, event.y)

        return


    def delete_selection(self):
        """
        Delete the current selection within the current project.

        """

        # Only do something if we have a current project and a non-empty
        # selection
        current = self.model_service.project
        selection = self.model_service.selection[:]
        if current is not None and len(selection) > 0:
            logger.debug('Deleting selection from Project [%s]', current)

            # Determine the context for the current project.  Raise an error
            # if we can't treat it as a context as then we don't know how
            # to delete anything.
            context = self._get_context_for_object(current)
            if context is None:
                raise Exception('Could not treat Project ' + \
                    '[%s] as a context' % current)

            # Filter out any objects in the selection that can NOT be deleted.
            deletables = []
            for item in selection:
                rt = self._get_resource_type_for_object(item.obj)
                nt = rt.node_type
                if nt.can_delete(item):
                    deletables.append(item)
                else:
                    logger.debug('Node type reports selection item [%s] is '
                        'not deletable.', nt)

            if deletables != []:
                # Confirm the delete operation with the user
                names = '\n\t'.join([b.name for b in deletables])
                message = ('You are about to delete the following selected '
                    'items:\n\t%s\n\n'
                    'Are you sure?') % names
                title = 'Delete Selected Items?'
                action = confirm(None, message, title)
                if action == YES:

                    # Unbind all the deletable nodes
                    if len(deletables) > 0:
                        self._unbind_nodes(context, deletables)

        return


    def is_current_project_saved(self, parent_window):
        """
        Give the user the option to save any modifications to the current
        project prior to closing it.

        If the user wanted to cancel the closing of the current project,
        this method returns False.  Otherwise, it returns True.

        """

        # The default is the user okay'd the closing of the project
        result = True

        # If the current project is dirty, handle that now by challenging the
        # user for how they want to handle them.
        current = self.model_service.project
        if not(self._get_project_state(current)):
            dialog = ConfirmationDialog(
                parent  = parent_window,
                cancel  = True,
                title   = 'Unsaved Changes',
                message = 'Do you want to save the changes to project "%s"?' \
                    % (current.name),
                )
            action = dialog.open()
            if action == CANCEL:
                result = False
            elif action == YES:
                result = self._save(current, parent_window)
            elif action == NO:
                # Delete the autosaved file as the user does not wish to
                # retain the unsaved changes.
                self._clean_autosave_location(current.location.strip())
        return result


    def listen_for_application_exit(self):
        """
        Ensure that we get notified of any attempts to, and thus have a chance
        to veto, the closing of the application.

        FIXME: Normally this should be called during startup of this
        plugin, however, Envisage won't let us find the workbench service
        then because we've made a contribution to its extension points
        and it insists on starting us first.

        """

        workbench = self.model_service.application.get_service('envisage.ui.workbench.workbench.Workbench')
        workbench.on_trait_change(self._workbench_exiting, 'exiting')

        return


    def open(self, event):
        """
        Open a project.

        """
        # Ensure any current project is ready for this change.
        if self.is_current_project_saved(event.window.control):

            # Query the user for the location of the project to be opened.
            path = self._show_open_dialog(event.window.control)
            if path is not None:
                logger.debug("Opening project from location [%s]", path)

                project = self.model_service.factory.open(path)
                if project is not None:
                    logger.debug("Opened Project [%s]", project.name)
                    self.model_service.project = project
                else:
                    msg = 'Unable to open %s as a project.' % path
                    error(event.window.control, msg, title='Project Open Error')

        return


    def save(self, event):
        """
        Save a project.

        """

        current = self.model_service.project
        if current is not None:
            self._save(current, event.window.control)

        return


    def save_as(self, event):
        """
        Save the current project to a different location.

        """

        current = self.model_service.project
        if current is not None:
            self._save(current, event.window.control, prompt_for_location=True)

        return


    #### protected interface #################################################

    def _auto_save(self, project):
        """

        Called periodically by the timer's Notify function to automatically
        save the current project.
        The auto-saved project has the extension '.autosave'.

        """
        # Save the project only if it has been modified.
        if project.dirty and project.is_save_as_allowed:
            location = project.location.strip()
            if not(location is None or len(location) < 1):
                autosave_loc = self._get_autosave_location(location)
                try:
                    # We do not want the project's location and name to be
                    # updated.
                    project.save(autosave_loc, overwrite=True,
                                 autosave=True)
                    msg = '[%s] auto-saved to [%s]' % (project,
                                                       autosave_loc)
                    logger.debug(msg)
                except:
                    logger.exception('Error auto-saving project [%s]'% project)
            else:
                logger.exception('Error auto-saving project [%s] in '
                                 'location %s' % (project, location))
        return


    def _clean_autosave_location(self, location):
        """
        Removes any existing autosaved files or directories for the project
        at the specified location.

        """
        autosave_loc = self._get_autosave_location(location)
        if os.path.exists(autosave_loc):
            self.model_service.clean_location(autosave_loc)
        return


    def _get_autosave_location(self, location):
        """
        Returns the path for auto-saving the project in location.

        """
        return os.path.join(os.path.dirname(location),
                            os.path.basename(location) + '.autosave')


    def _get_context_for_object(self, obj):
        """
        Return the context for the specified object.

        """

        if isinstance(obj, Context):
            context = obj
        else:
            context = None
            resource_type = self._get_resource_type_for_object(obj)
            if resource_type is not None:
                factory = resource_type.context_adapter_factory
                if factory is not None:
                    # FIXME: We probably should use a real environment and
                    # context (parent context?)
                    context = factory.adapt(obj, Context, {}, None)

        return context


    def _get_resource_type_for_object(self, obj):
        """
        Return the resource type for the specified object.

        If no type could be found, returns None.

        """

        resource_manager = self.model_service.resource_manager
        return resource_manager.get_type_of(obj)


    def _get_project_state(self, project):
        """ Returns True if the project is clean: i.e., the dirty flag is
        False and all autosaved versions have been deleted from the filesystem.

        """

        result = True
        if project is not None:
            autosave_loc = self._get_autosave_location(
                project.location.strip())
            if project.dirty or os.path.exists(autosave_loc):
                result = False
        return result


    def _get_user_location(self, project, parent_window):
        """
        Prompt the user for a new location for the specified project.

        Returns the chosen location or, if the user cancelled, an empty
        string.

        """

        # The dialog to use depends on whether we're prompting for a file or
        # a directory.
        if self.model_service.are_projects_files():
            dialog = FileDialog(parent = parent_window,
                title = 'Save Project As',
                default_path = project.location,
                action = 'save as',
                )
            title_type = 'File'
        else:
            dialog = DirectoryDialog(parent = parent_window,
                message = 'Choose a Directory for the Project',
                default_path = project.location,
                action = 'open'
                )
            title_type = 'Directory'

        # Prompt the user for a new location and then validate we're not
        # overwriting something without getting confirmation from the user.
        result = ""
        while(dialog.open() == OK):
            location = dialog.path.strip()

            # If the chosen location doesn't exist yet, we're set.
            if not os.path.exists(location):
                logger.debug('Location [%s] does not exist yet.', location)
                result = location
                break

            # Otherwise, confirm with the user that they want to overwrite the
            # existing files or directories.  If they don't want to, then loop
            # back and prompt them for a new location.
            else:
                logger.debug('Location [%s] exists.  Prompting for overwrite '
                    'permission.', location)
                message = 'Overwrite %s?' % location
                title = 'Project %s Exists' % title_type
                action = confirm(parent_window, message, title)
                if action == YES:

                    # Only use the location if we successfully remove the
                    # existing files or directories at that location.
                    try:
                        self.model_service.clean_location(location)
                        result = location
                        break

                    # Otherwise, display the remove error to the user and give
                    # them another chance to pick another location
                    except Exception as e:
                        msg = str(e)
                        title = 'Unable To Overwrite %s' % location
                        information(parent_window, msg, title)

        logger.debug('Returning user location [%s]', result)
        return result


    def _restore_from_autosave(self, project, autosave_loc):
        """ Restores the project from the version saved in autosave_loc.

        """

        workbench = self.model_service.application.get_service(
            'envisage.ui.workbench.workbench.Workbench')
        window = workbench.active_window
        app_name = workbench.branding.application_name
        message = ('The app quit unexpectedly when [%s] was being modified.\n'
                   'An autosaved version of this project exists.\n'
                   'Do you want to restore the project from the '
                   'autosaved version ?' % project.name)
        title = '%s-%s' % (app_name, project.name)
        action = confirm(window.control, message, title, cancel=True,
                         default=YES)
        if action == YES:
            try:
                saved_project = self.model_service.factory.open(autosave_loc)
                if saved_project is not None:
                    # Copy over the autosaved version to the current project's
                    # location, switch the model service's project, and delete
                    # the autosaved version.
                    loc = project.location.strip()
                    saved_project.save(loc, overwrite=True)
                    self.model_service.clean_location(autosave_loc)
                    self.model_service.project = saved_project
                else:
                    logger.debug('No usable project found in [%s].' %
                                 autosave_loc)
            except:
                logger.exception(
                    'Unable to restore project from [%s]' %
                    autosave_loc)
        self._start_timer(self.model_service.project)

        return


    def _save(self, project, parent_window, prompt_for_location=False):
        """
        Save the specified project.  If *prompt_for_location* is True,
        or the project has no known location, then the user is prompted to
        provide a location to save to.

        Returns True if the project was saved successfully, False if not.

        """

        location = project.location.strip()

        # If the project's existing location is valid, check if there are any
        # autosaved versions.
        autosave_loc = ''
        if location is not None and os.path.exists(location):
            autosave_loc = self._get_autosave_location(location)

        # Ask the user to provide a location if we were told to do so or
        # if the project has no existing location.
        if prompt_for_location or location is None or len(location) < 1:
            location = self._get_user_location(project, parent_window)
            # Rename any existing autosaved versions to the new project
            # location.
            if location is not None and len(location) > 0:
                self._clean_autosave_location(location)
                new_autosave_loc = self._get_autosave_location(location)
                if os.path.exists(autosave_loc):
                    shutil.move(autosave_loc, new_autosave_loc)

        # If we have a location to save to, try saving the project.
        if location is not None and len(location) > 0:
            try:
                project.save(location)
                saved = True
                msg = '"%s" saved to %s' % (project.name, project.location)
                information(parent_window, msg, 'Project Saved')
                logger.debug(msg)

            except Exception as e:
                saved = False
                logger.exception('Error saving project [%s]', project)
                error(parent_window, str(e), title='Save Error')
        else:
            saved = False

        # If the save operation was successful, delete any autosaved files that
        # exist.
        if saved:
            self._clean_autosave_location(location)
        return saved


    def _show_open_dialog(self, parent):
        """
        Show the dialog to open a project.

        """

        # Determine the starting point for browsing.  It is likely most
        # projects will be stored in the default path used when creating new
        # projects.
        default_path = self.model_service.get_default_path()
        project_class = self.model_service.factory.PROJECT_CLASS

        if self.model_service.are_projects_files():
            dialog = FileDialog(parent=parent, default_directory=default_path,
                title='Open Project')
            if dialog.open() == OK:
                path = dialog.path
            else:
                path = None
        else:
            dialog = DirectoryDialog(parent=parent, default_path=default_path,
                message='Open Project')
            if dialog.open() == OK:
                path = project_class.get_pickle_filename(dialog.path)
                if File(path).exists:
                    path = dialog.path
                else:
                    error(parent, 'Directory does not contain a recognized '
                        'project')
                    path = None
            else:
                path = None

        return path


    def _start_timer(self, project):
        """
        Resets the timer to work on auto-saving the current project.

        """

        if self.timer is None:
            if self.autosave_interval > 0:
                # Timer needs the interval in millisecs
                self.timer = Timer(self.autosave_interval*60000,
                                   self._auto_save, project)
        return


    def _unbind_nodes(self, context, nodes):
        """
        Unbinds all of the specified nodes that can be found within this
        context or any of its sub-contexts.

        This uses a breadth first algorithm on the assumption that the
        user will have likely selected peer nodes within a sub-context
        that isn't the deepest context.

        """

        logger.debug('Unbinding nodes [%s] from context [%s] within '
            'UiService [%s]', nodes, context, self)

        # Iterate through all of the selected nodes looking for ones who's
        # name is within our context.
        context_names = context.list_names()
        for node in nodes[:]:
            if node.name in context_names:

                # Ensure we've found a matching node by matching the objects
                # as well.
                binding = context.lookup_binding(node.name)
                if id(node.obj) == id(binding.obj):

                    # Remove the node from the context -AND- from the list of
                    # nodes that are still being searched for.
                    context.unbind(node.name)
                    nodes.remove(node)

                    # Stop if we've unbound the last node
                    if len(nodes) < 1:
                        break

        # If we haven't unbound the last node, then search any sub-contexts
        # for more nodes to unbind.
        else:

            # Build a list of all current sub-contexts of this context.
            subs = []
            for name in context.list_names():
                if context.is_context(name):
                    obj = context.lookup_binding(name).obj
                    sub_context = self._get_context_for_object(obj)
                    if sub_context is not None:
                        subs.append(sub_context)

            # Iterate through each sub-context, stopping as soon as possible
            # if we've run out of nodes.
            for sub in subs:
                self._unbind_nodes(sub, nodes)
                if len(nodes) < 1:
                    break


    def _workbench_exiting(self, event):
        """
        Handle the workbench polling to see if it can exit and shutdown the
        application.

        """

        logger.debug('Detected workbench closing event in [%s]', self)
        # Determine if the current project is dirty, or if an autosaved file
        # exists for this project (i.e., the project has changes which were
        # captured in the autosave operation but were not saved explicitly by
        # the user).  If so, let the user
        # decide whether to veto the closing event, save the project, or
        # ignore the dirty state.
        current = self.model_service.project

        if not(self._get_project_state(current)):
            # Find the active workbench window to be our dialog parent and
            # the application name to use in our dialog title.
            workbench = self.model_service.application.get_service('envisage.ui.workbench.workbench.Workbench')
            window = workbench.active_window
            app_name = workbench.branding.application_name

            # Show a confirmation dialog to the user.
            message = 'Do you want to save changes before exiting?'
            title = '%s - %s' % (current.name, app_name)
            action = confirm(window.control, message, title, cancel=True,
                default=YES)
            if action == YES:
                # If the save is successful, the autosaved file is deleted.
                if not self._save(current, window.control):
                    event.veto = True
            elif action == NO:
                # Delete the autosaved file as the user does not wish to
                # retain the unsaved changes.
                self._clean_autosave_location(current.location.strip())
            elif action == CANCEL:
                event.veto = True


    #### Trait change handlers ###############################################

    def _autosave_interval_changed(self, old, new):
        """
        Restarts the timer when the autosave interval changes.

        """

        self.timer = None
        if new > 0 and self.model_service.project is not None:
            self._start_timer(self.model_service.project)
        return


    def _project_changed_for_model_service(self, object, name, old, new):
        """
        Detects if an autosaved version exists for the project, and displays
        a dialog to confirm restoring the project from the autosaved version.

        """

        if old is not None:
            self.timer = None
        if new is not None:
            # Check if an autosaved version exists and if so, display a dialog
            # asking if the user wishes to restore the project from the
            # autosaved version.
            # Note: An autosaved version should exist only if the app crashed
            # unexpectedly. Regular exiting of the workbench should cause the
            # autosaved version to be deleted.
            autosave_loc = self._get_autosave_location(new.location.strip())
            if (os.path.exists(autosave_loc)):
                # Issue a do_later command here so as to allow time for the
                # project view to be updated first to reflect the current
                # project's state.
                do_later(self._restore_from_autosave, new,
                         autosave_loc)
            else:
                self._start_timer(new)
        return

#### EOF #####################################################################

