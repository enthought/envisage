""" A view proxy that lazily creates the actual view. """


# Enthought library imports.
from enthought.pyface.workbench.api import IView, View, WorkbenchWindow
from enthought.traits.api import Instance


class ViewProxy(View):
    """ A view proxy that lazily creates the actual view. """

    #### Private interface ####################################################

    # The view that we are a proxy for.
    _view = Instance(IView)

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################
    
    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the part.

        The parameter *parent* is the toolkit-specific control that is the 
        parts's parent.

        Return the toolkit-specific control.
        
        """

        return self._view.create_control(parent)
    
    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the part.

        Return None.
        
        """

        self._view.destroy_control()
        
        return
    
    def set_focus(self):
        """ Set the focus to the appropriate control in the part.

        Return None.

        """

        self._view.set_focus()

        return
    
    ###########################################################################
    # 'ViewProxy' interface.
    ###########################################################################

    def create_view(self):
        """ Create the actual view that we are a proxy for. """

        raise NotImplementedError

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait initializers ###################################################
    
    def __view_default(self):
        """ Trait initializer. """

        # Create the actual view...
        view = self.create_view()

        # ...and synchronize the proxy's traits with it.
        self._sync_traits_with_view(view)

        return view

    #### Methods ##############################################################

    def _sync_traits_with_view(self, view):
        """ Synchronize the proxy's traits with the actual view. """

        trait_names = [
            'control', 'has_focus', 'id', 'name', 'selection', 'window',
            'position', 'relative_to', 'width', 'height', 'busy', 'visible'
        ]

        for trait_name in trait_names:
            self.sync_trait(trait_name, view, mutual=True)
            #view.sync_trait(trait_name, self, mutual=True)

        return
    
### EOF #######################################################################

## # Enthought library imports.
## from enthought.pyface.workbench.api import IView, WorkbenchWindow
## from enthought.traits.api import Any, Bool, Enum, Float, HasTraits, Instance
## from enthought.traits.api import List, Str, Unicode, implements

## class ViewProxy(HasTraits):
##     """ A view proxy that lazily creates the actual view. """

##     implements(IView)
    
##     #### 'IWorkbenchPart' interface ###########################################
    
##     # The toolkit-specific control that represents the part.
##     #
##     # The framework sets this to the value returned by 'create_control'.
##     control = Any

##     # Does the part currently have the focus?
##     has_focus = Bool(False)

##     # The part's globally unique identifier.
##     id = Str

##     # The part's name (displayed to the user).
##     name = Unicode

##     # The current selection within the part.
##     selection = List

##     # The workbench window that the part is in.
##     #
##     # The framework sets this when the part is created.
##     window = Instance(WorkbenchWindow)

##     #### 'IPerspectiveItem' interface #########################################
        
##     # The position of the view relative to the item specified in the
##     # 'relative_to' trait.
##     #
##     # 'top'    puts the view above the 'relative_to' item.
##     # 'bottom' puts the view below the 'relative_to' item.
##     # 'left'   puts the view to the left of  the 'relative_to' item.
##     # 'right'  puts the view to the right of the 'relative_to' item.
##     # 'with'   puts the view in the same region as the 'relative_to' item.
##     #
##     # If the position is specified as 'with' you must specify a 'relative_to'
##     # item other than the editor area (i.e., you cannot position a view 'with'
##     # the editor area).
##     position = Enum('left', 'top', 'bottom', 'right', 'with')
    
##     # The Id of the view to position relative to. If this is not specified
##     # (or if no view exists with this Id) then the view will be placed relative
##     # to the editor area.
##     relative_to = Str
    
##     # The width of the item (as a fraction of the window width).
##     #
##     # e.g. 0.5 == half the window width.
##     #
##     # Note that this is treated as a suggestion, and it may not be possible
##     # for the workbench to allocate the space requested.
##     width = Float(-1)
    
##     # The height of the item (as a fraction of the window height).
##     #
##     # e.g. 0.5 == half the window height.
##     #
##     # Note that this is treated as a suggestion, and it may not be possible
##     # for the workbench to allocate the space requested.
##     height = Float(-1)

##     #### 'IView' interface ####################################################
    
##     # Is the view busy? (i.e., should the busy cursor (often an hourglass) be
##     # displayed?).
##     busy = Bool(False)

##     # Whether the view is visible or not.
##     visible = Bool(False)

##     #### Private interface ####################################################

##     # The view that we are a proxy for.
##     _view = Instance(IView)

##     ###########################################################################
##     # 'IWorkbenchPart' interface.
##     ###########################################################################

##     #### Trait initializers ###################################################

##     def _id_default(self):
##         """ Trait initialiser. """

##         # If no Id is specified then use the name.
##         return self.name
    
##     #### Methods ##############################################################
    
##     def create_control(self, parent):
##         """ Create the toolkit-specific control that represents the part.

##         The parameter *parent* is the toolkit-specific control that is the 
##         parts's parent.

##         Return the toolkit-specific control.
        
##         """

##         return self._view.create_control(parent)
    
##     def destroy_control(self):
##         """ Destroy the toolkit-specific control that represents the part.

##         Return None.
        
##         """

##         self._view.destroy_control()
        
##         return
    
##     def set_focus(self):
##         """ Set the focus to the appropriate control in the part.

##         Return None.

##         """

##         self._view.set_focus()

##         return
    
##     ###########################################################################
##     # 'ViewProxy' interface.
##     ###########################################################################

##     def create_view(self):
##         """ Create the actual view that we are a proxy for. """

##         raise NotImplementedError

##     ###########################################################################
##     # Private interface.
##     ###########################################################################

##     #### Trait initializers ###################################################
    
##     def __view_default(self):
##         """ Trait initializer. """

##         # Create the actual view and Synchronize the proxy's traits with it.
##         view = self.create_view()
##         self._sync_traits_with_view(view)

##         return view

##     #### Methods ##############################################################

##     def _sync_traits_with_view(self, view):
##         """ Synchronize the proxy's traits with the actual view. """

##         trait_names = [
##             'control', 'has_focus', 'id', 'name', 'selection', 'window',
##             'position', 'relative_to', 'width', 'height', 'busy', 'visible'
##         ]

##         for trait_name in trait_names:
##             self.sync_trait(trait_name, view, mutual=True)
##             #view.sync_trait(trait_name, self, mutual=True)

##         return
