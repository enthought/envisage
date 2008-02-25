""" The default workbench action set. """


# Enthought library imports.
from enthought.envisage.ui.action.api import Action, ActionSet, Group, Menu
from enthought.envisage.ui.action.api import ToolBar


class DefaultActionSet(ActionSet):
    """ The default workbench action set. """

    id = 'enthought.envisage.ui.workbench.default'
    
    menus = [
        Menu(
            name='&File', path='MenuBar',
            groups=['OpenGroup', 'SaveGroup', 'ImportGroup', 'ExitGroup']
        ),

        Menu(
            path='MenuBar',
            class_name='enthought.pyface.workbench.action.api:ViewMenuManager'
        ),

        Menu(
            name='&Tools', path='MenuBar',
            groups=['PreferencesGroup']
        ),
        
        Menu(
            name='&Help', path='MenuBar',
            groups=['AboutGroup']
        )
    ]

    actions = [
        Action(
            path='MenuBar/File', group='ExitGroup',
            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
        ),

        Action(
            path='MenuBar/Tools', group='PreferencesGroup',
            class_name='enthought.envisage.ui.workbench.action.api:EditPreferencesAction'
        ),
        
        Action(
            path='MenuBar/Help', group='AboutGroup',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),
    ]


class TestActionSet(ActionSet):
    """ An action test useful for testing. """

    id = 'enthought.envisage.ui.workbench.test'
    
    menus = [
        Menu(
            name='&Test', path='MenuBar',
            groups=['XGroup', 'YGroup']
        ),

        Menu(
            name='Foo', path='MenuBar/Test',
            groups=['XGroup', 'YGroup']
        ),

        Menu(
            name='Bar', path='MenuBar/Test',
            groups=['XGroup', 'YGroup']
        ),
    ]

    tool_bars = [
        ToolBar(name='Fred'),
        ToolBar(name='Wilma'),
        ToolBar(name='Barney')
    ]
        
    actions = [
        Action(
            path='ToolBar',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),
        
        Action(
            path='ToolBar',
            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
        ),

        Action(
            path='ToolBar/Fred',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),

        Action(
            path='ToolBar/Wilma',
            class_name='enthought.envisage.ui.workbench.action.api:AboutAction'
        ),
        
        Action(
            path='ToolBar/Barney',
            class_name='enthought.envisage.ui.workbench.action.api:ExitAction'
        )
    ]


    ###########################################################################
    # 'ActionSet' interface.
    ###########################################################################

##     @on_trait_change('enabled,visible')
##     def _state_changed(self, obj, trait_name, old, new):
##         """ Static trait change handler. """

##         self._update_tool_bars(obj, trait_name, new)
##         self._update_actions(obj, trait_name, new)

##         return

    def initialize(self, window):
        """ Called by the framework when the action set is added to a window.

        """

        print 'Initialize default action set!!!!!!!!!!!', self, window
        #self.test('enabled')
        
        return

    ###########################################################################
    # Testing interface.
    ###########################################################################

    def test(self, trait_name):
        """ Testing only! """

        def toggle(value):
            setattr(self, trait_name, value)

            GUI.invoke_after(500, toggle, not value)

            return

        from enthought.pyface.api import GUI
        GUI.invoke_after(1000, toggle, False)
        
        return

#### EOF ######################################################################
