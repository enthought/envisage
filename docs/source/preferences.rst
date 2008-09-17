
Preferences with Envisage
=========================

Envisage presents preferences with two different contributions:

  * PREFERENCES       = 'enthought.envisage.preferences'

  * PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'

The first one is only model-related and is for programmatic access to
preferences, whereas the second one is for displaying UIs to the user in
the workbench plugin.

Preferences
------------

The contribution point is simply a list of URLs to the preference file, eg::

  preferences_pages = List(
        ['pkgfile://acme.acmelab/preferences.ini'],
        contributes_to=PREFERENCES_PAGES)

where acme.acmelab is the python-module-like path to the package in which
the default preferences.ini is stored.


Preferences pages
------------------

The preference pages are a Traits UI view to wrap the preferences and
allow the user to modify them. A preference page is defined as in the
preference_manager example in the AppTools examples. It can than be
contributed to the workbench, as in::

    preferences_pages = List(contributes_to=PREFERENCES_PAGES)

    def _preferences_pages_default(self):
            """ Trait initializer. """
            from acme.preference_pages \
                            import ACMEPreferencePages
            return [ACMEPreferencePages, ]


