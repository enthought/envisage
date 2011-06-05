Last updated: 2006.02.05


BACKGROUND:
-----------
This plugin is designed to work with a single project at a time and build
up 'state' within that project until the user explicitly saves the project.

The plugin contributes two services to an Envisage application -- one for the
model and one for the UI.  Additionally, the plugin contributes a 'Project'
perspective, 'Project' view, and a number of actions to the UI so that the
user can create, open, save, save as, and close projects.  Finally, it should
be noted that the plugin manages an indicator applied to the application
window(s) titlebar as a representation that the current project has unsaved
modifications.

The current project is visualized using a ResourceTree control and thus
supports all the visualization and interaction customization of resources.
This also makes makes it easy to build a hierarchy of nodes within the tree
by implementing the apptools.naming.Context interface.

Finally, this plugin contributes a single extension point which provides the
capability to define your own custom projects.


PRE-REQUISITES:
---------------
This plugin requires the use of the envisage framework and the
following plugins:
        - envisage.core
        - envisage.resource
        - envisage.workbench
        - envisage.plugins.python_shell


HOW TO USE:
-----------
This plugin provides a base class for projects but, as of now, that class
has no capability to contain any data.  So for this plugin to be useful within
an Envisage application you have to complete the following:

- Contribute a project_plugin_definition.FactoryDefinition to the Envisage
  application.  This definition should point to a class derived from
  project_factory.ProjectFactory which will be used to create new projects
  as well as handle opening of persisted projects.  To do that, your
  ProjectFactory should override the 'create' and 'open' methods as
  appropriate to return an instance of a class derived from project.Project.
  Note that multiple plugins can contribute FactoryDefinitions but only the
  first contributed definition with the highest priority will be used.

- You will need to derive a class from project.Project which will be used to
  contain your project's data.  This class should:
    - override the trait_view trait to provide the UI content that will be
      shown by the plugin (within a wizard dialog) to allow a user to
      initialize a newly created project.
    - override the _contains_resource() method so that the plugin can close
      editors for resources in your project when your project closes.
    - set the 'dirty' trait to True anytime modifications are made to your
      project data
    - optionally override the Project.start() and Project.stop() methods
      to handle any work needing to be done when a project becomes the
      current project or is no longer the current project.  For example,
      the base Project uses the stop() method to close any editors associated
      with resources contained in the project.
    - optionally override the _load_hook() and _save() methods if you wish
      to use the base class's infrastructure for loading and saving projects
      but have additional work that needs to be accomplished during those
      events.  Note that the plugin's UI service calls the save() method and
      the ProjectFactory calls the load() method.
    - optionally override the 'load()' and 'save()' methods if you want to
      completely replace the base class's infrastructure for loading and
      saving projects.  Note that the plugin's UI service calls the save()
      method and the ProjectFactory calls the load() method.

- You will likely want to register resource types -- and associated classes
  such as node types, monitors, and resource references -- for the resources
  that can be contained within your project.  This will allow you to take
  maximum advantage of the infrastructure of the Project view's ResourceTree
  control.  If you do this, you should note that this plugin registers a
  ProjectResourceType, pointing to a ProjectNodeType, that is used to
  visualize the root project node.  You don't need to derive from these unless
  you want to customize the resource definition of the project node.

- Another option for implementing the visualization of project contents would
  be to derive from ProjectView and override the _create_project_control()
  and _update_project_control() methods to replace the ResourceTree control
  with some other UI control.  If you do the later, you will likely need to
  create your own project plugin definition but you should be able to reuse
  almost all of the infrastructure classes contained in this plugin.

- If the resources within your project can be edited in Editors, you should
  derive Editor classes from ProjectEditor so that the project plugin
  framework can close these editors when the project closes.


KNOWN ISSUES:
-------------
- Due to the current capabilities of the workbench plugin, this plugin can't
  do the ideal closing hook whereby, if the current project is modified, the
  user gets prompted to save it, close it, or cancel the closing of the window.
  The best we can do is follow the prompt to close the workbench window with a
  dialog querying the user whether they want to save the current project or
  not.  There is an Enthought Trac ticket to add the necessary capability to
  the workbench plugin and this plugin will be 'fixed' shortly thereafter.

- The Project class doesn't support any sort of versioning framework in its
  saving and loading.  This will cause problems as the content and
  capabilities of projects evolve throughout the software development cycle
  of an application that uses this plugin.


TO-DO:
------
- It would be nice if the Project class was modified such that it could
  actually be used without needing to be derived from.  One possibility for
  this would be to make it a full-fledged folder type Context in and of
  itself including support for binding and unbinding.  If this was done, it
  should be easy enough to re-use resource types, node types, etc. defined
  for other Envisage plugins within projects.

- It might be nice if editors that were open when a project was saved were
  restored when the project was re-loaded.  One mechanism to do this would
  be to modify the Project._editors trait to contain ResourceReferences rather
  than Resources as the keys.  Then when pickling, we would simple dump the
  editor references and persist just these keys.  Upon loading, iterate through
  the keys/resource references and open an editor for each.  One question about
  this mechanism is that currently we don't track order or position of editors
  so that info wouldn't be recovered.
