# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Utility functions for working with Python Eggs. """


# 3rd party imports.
import pkg_resources

# Enthought library imports.
from traits.util.toposort import topological_sort


def add_eggs_on_path(working_set, path, on_error=None):
    """Add all eggs found on the path to a working set."""

    environment = pkg_resources.Environment(path)

    # 'find_plugins' identifies those distributions that *could* be added
    # to the working set without version conflicts or missing requirements.
    distributions, errors = working_set.find_plugins(environment)
    if len(errors) > 0:
        if on_error:
            on_error(errors)
        else:
            raise RuntimeError("Cannot find eggs %s" % errors)

    # Add the distributions to the working set (this makes any Python
    # modules in the eggs available for importing).
    for distribution in distributions:
        working_set.add(distribution)


def get_entry_points_in_egg_order(working_set, entry_point_name):
    """Return entry points in Egg dependency order."""

    # Find all distributions that actually contain contributions to the
    # entry point.
    distributions = get_distributions_with_entry_point(
        working_set, entry_point_name
    )

    # Order them in dependency order (i.e. ordered by their requirements).
    distributions = get_distributions_in_egg_order(working_set, distributions)

    entry_points = []
    for distribution in distributions:
        entry_map = distribution.get_entry_map(entry_point_name)
        entry_points.extend(list(entry_map.values()))

    return entry_points


def get_distributions_with_entry_point(working_set, entry_point_name):
    """Return all distributions that contribute to an entry point."""

    distributions = []
    for distribution in working_set:
        if len(distribution.get_entry_map(entry_point_name)) > 0:
            distributions.append(distribution)

    return distributions


def get_distributions_in_egg_order(working_set, distributions=None):
    """Return all distributions in Egg dependency order."""

    # If no specific list of distributions is specified then use all
    # distributions in the working set.
    if distributions is None:
        distributions = working_set

    # Build a dependency graph.
    graph = {}
    for distribution in distributions:
        arcs = graph.setdefault(distribution, [])
        arcs.extend(get_requires(working_set, distribution))

    distributions = topological_sort(graph)
    distributions.reverse()

    return distributions


def get_requires(working_set, distribution):
    """Return all of the other distributions that a distribution requires."""

    requires = []
    for requirement in distribution.requires():
        required = working_set.find(requirement)
        # fixme: For some reason, the resolution of requirements sometimes
        # results in 'None' being returned instead of a distribution.
        if required is not None:
            requires.append(working_set.find(requirement))

    return requires
