""" Utility functions for working with Python Eggs. """


# Standard library imports.
import pkg_resources
import collections

# Enthought library imports.
from traits.util.toposort import topological_sort


class OrderedEntryPoint(pkg_resources.EntryPoint):
    """Overridden to use an ordered dict.  This preserves the order
    of the entry points and is useful for preserving the plugin order.
    """
    @classmethod
    def parse_group(cls, group, lines, dist=None):
        """Parse an entry point group"""
        if not pkg_resources.MODULE(group):
            raise ValueError("Invalid group name", group)
        this = collections.OrderedDict()
        for line in pkg_resources.yield_lines(lines):
            ep = cls.parse(line, dist)
            if ep.name in this:
                raise ValueError("Duplicate entry point", group, ep.name)
            this[ep.name]=ep
        return this


def get_ordered_entry_map(distribution, group=None):
    """Given a `distribution` this returns an ordered dictionary for the entry
    map for `group`, or the full entry map.

    Overridden Distribution.get_entry_map to use an `OrderedEntryPoint` 
    instead of the default unordered `EntryPoint`.
    
    """
    try:
        ep_map = distribution._ep_map
    except AttributeError:
        ep_map = distribution._ep_map = OrderedEntryPoint.parse_map(
            distribution._get_metadata('entry_points.txt'), distribution
        )
    if group is not None:
        return ep_map.get(group, collections.OrderedDict())
    return ep_map
    

def add_eggs_on_path(working_set, path):
    """ Add all eggs found on the path to a working set. """

    environment = pkg_resources.Environment(path)

    # 'find_plugins' identifies those distributions that *could* be added
    # to the working set without version conflicts or missing requirements.
    distributions, errors = working_set.find_plugins(environment)
    if len(errors) > 0:
        raise SystemError('Cannot find eggs %s' % errors)

    # Add the distributions to the working set (this makes any Python
    # modules in the eggs available for importing).
    map(working_set.add, distributions)
    
    return


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
        ep_map = get_ordered_entry_map(distribution, entry_point_name)
        entry_points.extend(ep_map.values())

    return entry_points


def get_distributions_with_entry_point(working_set, entry_point_name):
    """ Return all distributions that contribute to an entry point.

    """

    distributions = []
    for distribution in working_set:
        if len(get_ordered_entry_map(distribution, entry_point_name)) > 0:
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
