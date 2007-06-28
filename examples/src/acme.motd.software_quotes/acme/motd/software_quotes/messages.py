""" Extensions contributed by the plugin. """


# Plugin definition imports (extension points etc).
from acme.motd.api import Message


# These are all contributions to the 'Message' extension point.
meyer = Message(
    author = "Bertrand Meyer",
    text   = "You can have quality software, or you can have pointer"
    " arithmetic; but you cannot have both at the same time."
)

dijkstra = Message(
    author = "Edgar W. Dijkstra",
    text   = "The effective programmer is keenly aware of the limited size"
    " of his own head."
)

fuller = Message(
    author = "Richard Buckminster-Fuller",
    text   = "When I'm working on a problem, I never think about beauty. I"
    " think only how to solve the problem. But when I have finished, if"
    " the solution is not beautiful, I know it is wrong."
)

gilb = Message(
    author = "Tom Gilb",
    text   = "If you don't know what you're doing, don't do it on a large"
    " scale."
)

norman = Message(
    author = "Arthur Norman",
    text   = "The best way to implement hard code is never to know you're"
    " implementing it."
)

einstein = Message(
    author = "Albert Einstein",
    text   = "Any intelligent fool can make things bigger, more complex,"
    " and more violent. It takes a touch of genius - and a lot of courage"
    " - to move in the opposite direction."
)

fowler = Message(
    author = "Martin Fowler",
    text   = "Any fool can write code that a computer can understand. Good"
    " programmers write code that humans can understand."
)

hendrickson = Message(
    author = "Chet Hendrickson",
    text   = "The rule is, 'Do the simplest thing that could possibly"
    " work', not the most stupid."
)

jeffries = Message(
    author = "Ron Jeffries",
    text   = "If you're working sixty hour weeks, you're too tired to be"
    " doing good software."
)

tuft = Message(
    author = "Edward Tufte",
    text   = "Clutter and confusion are failures of design, not attributes"
    " of information. There's no such thing as information overload."
)

#### EOF ######################################################################
