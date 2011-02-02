# Enthought library imports.
from enthought.traits.api import Callable, HasTraits, Str, Unicode


class TaskFactory(HasTraits):
    """ A factory for creating a Task with some additional metadata.
    """

    # The task factory's unique identifier. This ID is assigned to all tasks
    # created by the factory.
    id = Str

    # The task factory's user-visible name. As above, this is assigned to all
    # tasks created by the factory.
    name = Unicode

    # A callable with the following signature:
    #
    #     callable(**traits) -> Task
    #
    # Often this attribute will simply be a subclass of Task.
    factory = Callable

    def create(self, **traits):
        """ Creates the Task.

        The default implementation simply calls the 'factory' attribute.
        """
        return self.factory(**traits)
