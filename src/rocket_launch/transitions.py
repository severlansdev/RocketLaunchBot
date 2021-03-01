# coding: utf-8
from bernard.engine import (
    Tr,
    triggers as trg,
)
from bernard.i18n import (
    intents as its,
)

from bernard.platforms.telegram import (
    layers as tl,
)

from .states import *
from .trigger import RocketLaunched

transitions = [
    # Entry point for the /start command
    Tr(
        dest=Welcome,
        factory=trg.Equal.builder(tl.BotCommand('/start')),
    ),
    # The user starts guessing
    Tr(
        dest=Guess,
        origin=Welcome,
        factory=trg.Action.builder('start'),
    ),
    # The user decides not to play
    Tr(
        dest=Quit,
        origin=Welcome,
        factory=trg.Action.builder('no_start'),
    ),
    # After the guessing first step, it goes to Check_again
    Tr(
        dest=Check_again, 
        origin=Guess, 
        factory=RocketLaunched.builder(is_finished=False)
    ),

    # Keep searching if the frame is not yet found
    Tr(
        dest=Check_again, 
        origin=Check_again, 
        factory= RocketLaunched.builder(is_finished=False)
    ),

    # Stop searching when the frame is found
    Tr(
        dest=Finish, 
        origin=Check_again, 
        factory= RocketLaunched.builder(is_finished=True)
    ),           
    
    # Restart after finishing
    Tr(
        dest=Welcome,
        origin=Finish,
        factory=trg.Action.builder('restart'),
    ),

    # Quit the game when finishing
    Tr(
        dest=Quit,
        origin=Finish,
        factory=trg.Action.builder('no_restart'),
    ),

]
