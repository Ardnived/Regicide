'''
Created on Apr 13, 2013

@author: Devindra

The controller information used in menu views.

TODO: rename this file
'''
from functools import partial
from pyglet.window import key
from regicide.controller.commands import CommandSet, KeyBinder, KeyBinding
from regicide.controller import functions

commands = CommandSet({
    'exit': KeyBinder(
        bindings = [
            KeyBinding(key.ENTER),
            KeyBinding(key.ESCAPE),
        ],
        action = partial(functions.set_state, state='game'),
    ),
})