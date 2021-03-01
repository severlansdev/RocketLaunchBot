from bernard import (
    layers as lyr,
)
from bernard.engine.triggers import (
    BaseTrigger,
)

from .store import (
    cs,
)


class RocketLaunched(BaseTrigger):
    """
    This trigger will try choose the images to show.  The method to detect the next images uses the
    bisection method. The 'is_finished' parameter allow the trigger to activate to return the guessed date
    """

    def __init__(self, request, is_finished):
        super().__init__(request)
        self.is_finished = is_finished

    # noinspection PyMethodOverriding
    @cs.inject()
    async def rank(self, context) -> float:
      
        try:
            payload = self.request.get_layer(lyr.Postback).payload
        except (KeyError, ValueError, TypeError):
            return .0 

        # Sanity check
        left_index = context.get('left_index')
        right_index = context.get('right_index')
        if left_index is None or right_index is None:
            return .0
      
        if left_index + 1  >= right_index:
            is_finished = True
            print('Finished count')
        else:
            is_finished = False
            print('Unfinished count')

        return 1. if is_finished == self.is_finished else .0


