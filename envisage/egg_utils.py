""" Utility functions for working with Python Eggs. """


# Standard library imports.
import pkg_resources

# Enthought library imports.
from traits.util.graph import topological_sort



def get_entry_points_in_egg_order(working_set, entry_point_name):
    """ Return entry points in Egg dependency order. """

    # Find all distributions that actually contain contributions to the
    # entry point.
    distributions = get_distributions_with_entry_point(
        working_set, entry_point_name
    )

    # Order them in dependency order (i.e. ordered by their requirements).
    distributions = get_distributions_in_egg_order(working_set, distributions)

    entry_points = []
    for distribution in distributions:
        map = distribution.get_entry_map(entry_point_name)
        entry_points.extend(map.values())

    return entry_points


def get_distributions_with_entry_point(working_set, entry_point_name):
    """ Return all distributions that contribute to an entry point.

    """

    distributions = []
    for distribution in working_set:
        if len(distribution.get_entry_map(entry_point_name)) > 0:
            distributions.append(distribution)

    return distributions


def get_distributions_in_egg_order(working_set, distributions=None):
    """ Return all distributions in Egg dependency order. """

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
    """ Return all of the other distributions that a distribution requires. """

    requires = []
    for requirement in distribution.requires():
        required = working_set.find(requirement)
        # fixme: For some reason, the resolution of requirements sometimes
        # results in 'None' being returned instead of a distribution.
        if required is not None:
            requires.append(working_set.find(requirement))

    return requires

#### EOF ######################################################################
