# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Primary API for envisage

Interfaces
----------

- :class:`~.IApplication`
- :class:`~.IExtensionPoint`
- :class:`~.IExtensionPointUser`
- :class:`~.IExtensionProvider`
- :class:`~.IExtensionRegistry`
- :class:`~.IImportManager`
- :class:`~.IPlugin`
- :class:`~.IPluginActivator`
- :class:`~.IPluginManager`
- :class:`~.IServiceRegistry`

Constants
---------
- :data:`~.BINDINGS`
- :data:`~.COMMANDS`
- :data:`~.PREFERENCES`
- :data:`~.PREFERENCES_CATEGORIES`
- :data:`~.PREFERENCES_PANES`
- :data:`~.SERVICE_OFFERS`
- :data:`~.TASKS`
- :data:`~.TASK_EXTENSIONS`

Application, plugin and related classes
---------------------------------------
- :class:`~.Application`
- :class:`~.CorePlugin`
- :class:`~.EggPluginManager`
- :class:`~.ExtensionPoint`
- :class:`~.ExtensionPointBinding`
- :func:`~.bind_extension_point`
- :func:`~.unbind_extension_point`
- :class:`~.ExtensionProvider`
- :class:`~.ExtensionPointChangedEvent`
- :class:`~.ImportManager`
- :class:`~.Plugin`
- :class:`~.PluginActivator`
- :class:`~.PluginExtensionRegistry`
- :class:`~.PluginManager`
- :class:`~.ProviderExtensionRegistry`
- :class:`~.Service`
- :class:`~.ServiceOffer`
- :class:`~.ServiceRegistry`

Exceptions
----------

- :class:`~.NoSuchServiceError`
- :class:`~.UnknownExtension`
- :class:`~.UnknownExtensionPoint`

"""

from .application import Application
from .core_plugin import CorePlugin
from .egg_plugin_manager import EggPluginManager
from .extension_point import ExtensionPoint
from .extension_point_binding import (
    bind_extension_point,
    ExtensionPointBinding,
    unbind_extension_point,
)
from .extension_point_changed_event import ExtensionPointChangedEvent
from .extension_provider import ExtensionProvider
from .extension_registry import ExtensionRegistry
from .i_application import IApplication
from .i_extension_point import IExtensionPoint
from .i_extension_point_user import IExtensionPointUser
from .i_extension_provider import IExtensionProvider
from .i_extension_registry import IExtensionRegistry
from .i_import_manager import IImportManager
from .i_plugin import IPlugin
from .i_plugin_activator import IPluginActivator
from .i_plugin_manager import IPluginManager
from .i_service_registry import IServiceRegistry
from .ids import (
    BINDINGS,
    COMMANDS,
    PREFERENCES,
    PREFERENCES_CATEGORIES,
    PREFERENCES_PANES,
    SERVICE_OFFERS,
    TASK_EXTENSIONS,
    TASKS,
)
from .import_manager import ImportManager
from .plugin import Plugin
from .plugin_activator import PluginActivator
from .plugin_extension_registry import PluginExtensionRegistry
from .plugin_manager import PluginManager
from .provider_extension_registry import ProviderExtensionRegistry
from .service import Service
from .service_offer import ServiceOffer
from .service_registry import NoSuchServiceError, ServiceRegistry
from .unknown_extension import UnknownExtension
from .unknown_extension_point import UnknownExtensionPoint
