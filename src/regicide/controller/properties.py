'''
Created on Apr 13, 2013

@author: Devindra
'''
from functools import partial
from pyglet.window import key
from regicide.controller.commands import CommandSet, KeyBinder, KeyBinding
from regicide.controller import functions

commands = CommandSet({
    'exit': KeyBinder(
        bindings = [
            KeyBinding(key.ENTER),
        ],
        action = partial(functions.set_state, state='game'),
    ),
})