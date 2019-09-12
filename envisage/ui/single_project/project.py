# (C) Copyright 2007-2019 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
"""
A base class for projects that can be displayed by the single_project
plugin.

"""

# Standard library imports.
import logging
import os
import sys

# Enthought library imports
from traits.etsconfig.api import ETSConfig
import apptools.sweet_pickle
from apptools.io.api import File
from traits.api import Any, Bool, Dict, Directory, HasTraits, \
    Instance, Property, Str
from traitsui.api import Group, View
from traits.util.clean_strings import clean_filename

# Local imports.
#from envisage.ui.single_project.editor.project_editor import \
#    ProjectEditor
from envisage.api import Application


# Setup a logger for this module.
logger = logging.getLogger(__name__)


class Project(HasTraits):
    """
    A base class for projects that can be displayed by the single_project
    plugin.

    """

    ##########################################################################
    # CLASS Attributes
    ##########################################################################

    #### public 'Project' class interface ####################################

    # Indicates whether instances of this project class are stored as files or
    # directories.  The rest of the single_project plugin will follow this
    # setting when using this project class.
    #
    # This is meant to be a constant for the lifetime of this class!
    PROJECTS_ARE_FILES = True

    # Current envisage application.
    application = Instance(Application, transient=True)


    #### protected 'Project' class interface #################################

    # Format used to create a unique name from a location and a counter.
    _unique_name_format = '%s_%s'


    ##########################################################################
    # Attributes
    ##########################################################################

    #### public 'Project' interface ##########################################

    # True if this project contains un-saved state (has been modified.)
    dirty = Bool(False, transient=True)

    # True if we allow save requests on the project.
    is_save_allowed = Bool(True, transient=True)

    # True if we allow save_as requests on the project.
    is_save_as_allowed = Bool(True, transient=True)

    # The location of this project on the filesystem.  The default value
    # depends on the runtime environment so we use a traits default method to
    # set it.
    location = Directory

    # The name of this project.  This is calculated from the project's current
    # location or, if there is no location, from a default value.  See the
    # property's getter method.
    name = Property(Str)

    # The UI view to use when creating a new project
    traits_view = View(
        Group('location'),
        title = 'New Project',
        id = 'envisage.single_project.project.Project',
        buttons = [ 'OK', 'Cancel' ],
        width = 0.33,

        # Ensure closing via the dialog close button is the same
        # as clicking cancel.
        close_result = False,

        # Ensure the user can resize the dialog.
        resizable = True,
        )


    #### protected 'Project' interface #######################################

    # A list of editors currently open to visualize our resources
    # FIXME: Re-add the ProjectEditor's(if we need them) once they are fixed.
    #_editors = Dict(Any, ProjectEditor, transient=True)

    # The cache of this project's name.  We can't just initialize it to a
    # default value since the location may be cleared at any time.
    _name = Str(transient=True)


    ##########################################################################
    # 'Object' interface.
    ##########################################################################

    #### operator methods ####################################################

    def __getstate__(self):
        """
        Get the state of this object for pickling.

        Extended to limit which attributes get pickled and also to add
        version numbers to our pickle.

        It is STRONGLY recommended that derived classes not leverage the
        pickling mechanism if they wish to store additional data in OTHER
        files as part of their project.  Instead, they should override the
        *_save* method.

        Extending this method in derived classes IS appropriate if you want
        to store additional data in the SAME pickle file as the project.

        """

        # Determine the starting point for our state.
        state = super(Project, self).__getstate__().copy()

        # Remove any transient traits.
        for trait_name in self.trait_names(transient=True):
            state.pop(trait_name, None)

        # Add in our current version number.  Note use a different attribute
        # name from any base or derived class so that our numbers don't
        # override theirs.
        state['_project_version_major'] = 1
        state['_project_version_minor'] = 0

        return state


    def __setstate__(self, state):
        """
        Restore the state of this object during unpickling.

        Extended to upgrade pickles to the current Project version.

        It is STRONGLY recommended that derived classes not leverage the
        unpickling mechanism if they wish to load data from additional pickle
        files. Instead, they should override the *_load* method.

        Extending this method in derived classes IS appropriate if you want
        to load additional data from the SAME pickle file as the project.

        """

        # Get the version info out of the state dictionary.
        major = state.pop('_project_version_major', 0)
        minor = state.pop('_project_version_minor', 0)

        # Upgrade to version 1.
        if major < 1:

            # Remove any old attributes.
            # - name is now a calculated property instead of stored value.
            for key in ['name']:
                state.pop(key, None)

        # Restore our state.
        return super(Project, self).__setstate__(state)


    def __str__(self):
        """
        Return the unofficial string representation of this object.

        """

        result ='%s(name=%s)' % (super(Project, self).__str__(), self.name)
        return result


    ##########################################################################
    # 'Project' interface.
    ##########################################################################

    #### public interface ####################################################

    def get_default_project_location(self, application):
        """
        Return the default location for a new project.

        """

        path = self.get_default_path(application)
        name = clean_filename(self.get_default_name())
        location = os.path.join(path, name)
        location = self._make_location_unique(location)

        return location

    def get_default_path(cls, application):
        """
        Return the default path to the parent directory for a new project.

        """

        # When unpickling, we don't have a reference to the current application, so we
        # fallback on application_home.
        if application is None:
            return ETSConfig.application_home

        app_preferences = application.preferences
        path_id = 'envisage.ui.' \
            'single_project.preferred_path'
        path = app_preferences.get(path_id)

        # If the 'preferred_path' variable isn't set in the user's preferences,
        # then we set to the the application home by default.
        if len(path) == 0:
            app_home = ETSConfig.application_home
            app_preferences.set(path_id, app_home)
            return app_home

        return path

    get_default_path = classmethod(get_default_path)

    def get_default_name(self):
        """
        Return the default name for a new project.

        """

        return 'New Project'

    def get_pickle_filename(cls, location):
        """
        Generate the project's pickle filename given a source location.

        By default, the filename IS the specified location or, when saving
        projects as directories, a file called 'project' within a directory
        that is the specified location,

        Derived classes may wish to use the location as the basis for
        identifying the real pickle file.

        """

        if cls.PROJECTS_ARE_FILES:
            result = location
        else:
            result = os.path.join(location, 'project')

        return result

    get_pickle_filename = classmethod(get_pickle_filename)

    def get_pickle_package(cls):
        """
        Returns the pickle package to use for pickling and unpickling
        projects.

        Implementors can override this to customize the way in which
        projects are pickled and unpickled.

        This implementation returns the apptools.sweet_pickle package which
        supports versioning and refactoring of classes.

        """

        return apptools.sweet_pickle

    get_pickle_package = classmethod(get_pickle_package)

    def load(cls, location, application):
        """
        Load a project from a specified location.

        The loaded project's location is always set to the location the project
        was actually loaded from.  Additionally, the dirty flag is cleared
        on the loaded project.

        An exception will be raised to indicate a failure.

        """

        # Load the project in a manner that derived classes can modify.
        project = cls._load(location)

        # Ensure the project's location reflects where the project was loaded
        # from and that the dirty flag is not set.
        project.location = location
        project.dirty = False

        # Set the project's 'application' to the running application passed in.
        project.application = application

        return project

    load = classmethod(load)

    def register_editor(self, resource, editor, remove=False):
        """
        Inform us that an editor has been opened for what is believed to be
        a resource in this project.

        Note that if this project can be represented as a hierarchy, the
        resource may not be a top level object in that hierarchy!

        """

        # Warn if the resource is not part of this project
        if not self._contains_resource(resource):
            logger.warning(
                'This Project [%s] does not contain resource [%s]',
                self, resource)

        # Add or remove from our set of editors as requested
        if not remove:
            self._editors[resource] = editor
        else:
            del self._editors[resource]


    def save(self, location=None, overwrite=False):
        """
        Save this project.

        The project is saved to its current location, identified by the value
        of the *location* trait, unless a new location is explicitly provided.
        The specification of a new location is used to do a 'save as'
        operation.

        If a new location is provided, and a file or directory already exists
        at that location, then an *AssertionError* exception is raised unless
        the overwrite flag is True.  This ensures that users won't accidentally
        overwrite existing data.

        This method requires the overwrite flag because prompting the user to
        confirm the overwrite requires GUI interaction and thus should not be
        done at the model level.

        Note that, because we can rely on the location of a loaded project
        always being set to the location it was loaded from, there is no reason
        to try to force the *location* trait within a saved project to the
        location we are trying to save to.  Instead, we update the value in
        the in-memory version of the project only if the save completed
        successfully.

        The dirty flag is always cleared upon a succesfull save of the project.

        An exception will be raised to indicate a failure.

        """

        # Ensure saving (or save as) is allowed at this time.
        if location is None or location == self.location:
            if not self.is_save_allowed:
                raise AssertionError('Saving is currently not allowed.')
        elif location != self.location:
            if not self.is_save_as_allowed:
                raise AssertionError('Save as is currently not allowed.')

        # Use the internally-specified location unless a new location was
        # explicitly provided.  The new location can not contain any starting
        # or trailing whitespace and it cannot overwrite an existing file or
        # directory unless that was explicitly allowed.
        loc = self.location
        if location is not None:
            location = location.strip()
            if len(location) > 0 and location != self.location:

                # Ensure we never overwrite existing files / directories just
                # because someone specified a new location.  (Confirmation or
                # correction of overwriting requires prompting of the user and
                # is thus not part of the project model.)
                if os.path.exists(location) and overwrite is False:
                    raise AssertionError('Can not overwrite existing ' + \
                        'location [%s]' % location)

                # The requested location is valid so let's use it.
                loc = location

        # Ensure all necessary directories exist.  If we're saving a file, then
        # these are the path upto the file name.  If we're saving to a directory
        # then the path is the complete location.
        if self.PROJECTS_ARE_FILES:
            path, filename = os.path.split(loc)
        else:
            path = loc
        if len(path) > 0:
            f = File(path)
            if f.is_file:
                f.delete()
            if not f.exists:
                f.create_folders()

        # Save this project in a manner that derived classes can modify.
        self._save(loc)

        # If the save succeeds (no exceptions were raised), then update the
        # location of the project and clear the dirty flag.
        self.location = loc
        self.dirty = False

        return


    def start(self):
        """
        Notify this project that it is now the 'current' project.

        This call should only be made by the project plugin framework!

        This call *could* happen multiple times to a project, but
        only if interwoven with paired calls to the 'stop' method.

        Derived classes should override this, and chain the base
        implementation, if they need to do anything when a project
        becomes current.

        """

        logger.debug('Project [%s] started', self)

        # Ensure we start with an empty set of editors
        self._editors = {}


    def stop(self):
        """
        Called only by the project plugin framework to notify this
        project it is no longer the current project.

        This call *could* happen multiple times to a project, but
        only if interwoven with paired calls to the 'start' method.

        Derived classes should override this, and chain the base
        implementation, if they need to do anything when a project
        stops being current.

        """

        # Close all of the editors displaying our resources
        self._close_all_editors()

        logger.debug('Project [%s] stopped', self)


    #### protected interface #################################################

    def _close_all_editors(self):
        """
        Called to close all editors associated with this project.

        """

        # NOTE: The close() method on the editor will call back to remove
        # itself from our set of registered editors.  (This assumes the
        # editor is derived from ProjectEditor.)
        for editor in self._editors.values():
            logger.debug('Project requesting close of ProjectEditor [%s]',
                editor)
            editor.close()


    def _close_resource_editors(self, resource):
        """
        Close any editors associated with the specified resource(s).

        The passed value may be a single resource or a list of resources.  The
        resources should be parts of this project but no error is generated if
        they are not, nor if they are not currently associated with an editor.

        """

        # Ensure we're dealing with a list of resources.
        if not isinstance(resource, list):
            resource = [resource]

        # Close any editors associated with the resources
        for r in resource:
            editor = self._editors.get(r, None)
            if editor is not None:
                logger.debug('Requesting close of ProjectEditor [%s] from ' + \
                    'Project [%s]', editor, self)
                editor.close()

        return


    def _contains_resource(self, resource):
        """
        Called to determine if this project contains the specified
        resource.

        Note that if this project can be represented as a hierarchy, the
        resource may not be a top level object in that hierarchy!

        Derived classes must implement this!

        """

        return False


    def _get_name(self):
        """
        Returns the current name for this project.

        The name is always the last part of the path that is the project's
        location.  If we have no location, then a default name is returned.

        """

        # Prefer to use the cached version of the name
        if self._name is not None and len(self._name) > 0:
            result = self._name

        # Use (and cache) a name from our current location
        else:
            # Strip any trailing path separator off the current location so
            # that we use the last directory name if our location is a
            # directory
            location = self.location.rstrip(os.path.sep)

            # The project name is then the basename of the location
            self._name = os.path.basename(location)
            result = self._name

        return result


    def _load(cls, location):
        """
        Load a project from the specified location.

        This method exists purely to allow derived classes to have an easy way
        to override or extend the loading of a project.  The default behavior
        is to load the project from a file using the unpickle mechanism.

        The caller is notified of loading errors by raised exceptions.

        """

        # Allow derived classes to determine the actual pickle file given the
        # requested source location.
        filename = cls.get_pickle_filename(location)
        logger.debug('Loading Project of class [%s] from [%s]', cls,
            filename)

        # Try to unpickle the project while making sure to close any file we
        # opened.
        fh = None
        try:
            fh = open(filename, 'rb')
            pickle_package = cls.get_pickle_package()
            project = pickle_package.load(fh)

            # Allow derived classes to customize behavior after unpickling
            # is complete.
            project._load_hook(location)

            logger.debug('Loaded Project [%s] from location [%s]', project,
                filename)

        # Ensure any opened file is closed
        finally:
            if fh:
                try:
                    fh.close()
                except:
                    logger.exception('Unable to close project file [%s]',
                        filename)

        return project
    _load = classmethod(_load)


    def _load_hook(self, location):
        """
        Finish loading of a project.

        This method exists purely to allow derived classes to customize the
        steps that finish the loading of a project.

        Note that the project's internal location value does not yet reflect
        the location the project was loaded from, nor do we guarantee the dirty
        flag isn't set.  (Doing the right thing to both of these is done by the
        framework after this method!)

        """

        pass


    def _location_default(self):
        """
        Generates the default value for our location trait.

        """

        return self.get_default_project_location(self.application)


    def _make_location_unique(cls, location):
        """
        Return a location, based off the specified location, that does
        not already exist on the filesystem.

        """

        result = location
        counter = 1
        while os.path.exists(result):
            result = cls._unique_name_format % (location, counter)
            counter+=1

        return result
    _make_location_unique = classmethod(_make_location_unique)


    def _save(self, location):
        """
        Save this project to the specified location.

        This method exists purely to allow derived classes to have an easy way
        to override or extend the saving of a project.  The default behavior is
        to save this project to a file using the pickle mechanism.

        The caller is notified of saving errors by raised exceptions.

        """

        # Allow derived classes to determine the actual pickle file from the
        # specified location.
        filename = self.get_pickle_filename(location)
        logger.debug('Saving Project [%s] to [%s]', self, filename)

        # Pickle the object to a file while making sure to close any file we
        # open.  Note that we can't just log or ignore errors here as the
        # caller needs to know whether we succeeded or not, and could possibly
        # handle the exception if they knew what it was.
        fh = None
        try:
            # Allow derived classes to customize behavior before pickling is
            # applied.
            self._save_hook(location)

            fh = open(filename, 'wb')
            pickle_package = self.get_pickle_package()
            pickle_package.dump(self, fh, 1)

            logger.debug('Saved Project [%s] to [%s]', self, filename)
        finally:
            try:
                if fh is not None:
                    fh.close()
            except:
                logger.exception('Unable to close project pickle file [%s]',
                    filename)

        return


    def _save_hook(self, location):
        """
        Start saving a project.

        This method exists purely to allow derived classes to customize the
        steps that initiate the saving of a project.

        Note that the project's internal location value does not reflect the
        target location for the save.

        """

        pass


    #### trait handlers ######################################################

    def _location_changed(self, old, new):
        """
        Called whenever the project's location changes.

        """

        logger.debug('Location changed from [%s] to [%s] for Project [%s]',
            old, new, self)

        # Invalidate any cached project name
        old_name = self._name
        self._name = ''
        self.trait_property_changed('name', old_name, self.name)

        # Indicate this project is now dirty
        self.dirty = True


#### EOF #####################################################################
