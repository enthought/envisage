# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Some messages! """

from acme.motd.api import Message

messages = [
    Message(
        author="Bertrand Meyer",
        text="You can have quality software, or you can have pointer"
        " arithmetic; but you cannot have both at the same time.",
    ),
    Message(
        author="Edsger W. Dijkstra",
        text="The effective programmer is keenly aware of the limited size"
        " of his own head.",
    ),
    Message(
        author="Richard Buckminster-Fuller",
        text="When I'm working on a problem, I never think about beauty. I"
        " think only how to solve the problem. But when I have finished, if"
        " the solution is not beautiful, I know it is wrong.",
    ),
    Message(
        author="Tom Gilb",
        text="If you don't know what you're doing, don't do it on a large"
        " scale.",
    ),
    Message(
        author="Arthur Norman",
        text="The best way to implement hard code is never to know you're"
        " implementing it.",
    ),
    Message(
        author="Albert Einstein",
        text="Any intelligent fool can make things bigger, more complex,"
        " and more violent. It takes a touch of genius - and a lot of courage"
        " - to move in the opposite direction.",
    ),
    Message(
        author="Martin Fowler",
        text="Any fool can write code that a computer can understand. Good"
        " programmers write code that humans can understand.",
    ),
    Message(
        author="Chet Hendrickson",
        text="The rule is, 'Do the simplest thing that could possibly"
        " work', not the most stupid.",
    ),
    Message(
        author="Ron Jeffries",
        text="If you're working sixty hour weeks, you're too tired to be"
        " doing good software.",
    ),
    Message(
        author="Edward Tufte",
        text="Clutter and confusion are failures of design, not attributes"
        " of information. There's no such thing as information overload.",
    ),
]
