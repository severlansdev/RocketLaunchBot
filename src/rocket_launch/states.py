# coding: utf-8
from random import SystemRandom

from bernard import layers as lyr
from bernard.analytics import page_view
from bernard.engine import BaseState
from bernard.i18n import intents as its, translate as t

from bernard.platforms.telegram import layers as tl, media as media
from .store import cs

from bernard.media.base import UrlMedia
from .frames import get_video_url, get_frame_url, get_video_information
from .bisection import bisect

random = SystemRandom()


class RocketLaunchState(BaseState):
    """
    Root class for Rocket Launch.

    Here you must implement "error" and "confused" to suit your needs. They
    are the default functions called when something goes wrong. The ERROR and
    CONFUSED texts are defined in `i18n/en/responses.csv`.
    """

    @page_view('/bot/error')
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """
        self.send(lyr.Text(t.ERROR))

    @page_view('/bot/confused')
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """
        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError


class Welcome(RocketLaunchState):
    """
    Welcome state, asks the user to start guessing. If not, it will enter the Quit State
    """

    @page_view('/bot/welcome')
    async def handle(self) -> None:
        name = await self.request.user.get_friendly_name()

        self.send(
            lyr.Text(t('WELCOME', name=name)),
            tl.InlineKeyboard([
                [tl.InlineKeyboardCallbackButton(
                    text=t.START_PLAY,
                    payload={'action': 'start'})],
                [tl.InlineKeyboardCallbackButton(
                    text=t.QUIT_PLAY,
                    payload={'action': 'no_start'})]

            ])
        )


class Guess(RocketLaunchState):
    """
    First state for guessing, obtains the information about the video and configures the indexes. 
    Shows the user an image, and the user must decide if the rocket has launched yet or not. 
    """

    @page_view('/bot/guess')
    @cs.inject()
    async def handle(self, context) -> None:
        name = await self.request.user.get_friendly_name()
        # Get information about the images from the video
        frames = get_video_information()

        if frames:
            # Set context of indexes and frames for the video
            context['left_index'] = 0
            context['right_index'] = frames - 1
            # Get the new frame to show using the bisection method
            context['left_index'], context['right_index'], frame_number = bisect(
                int(context.get('left_index')), int(context.get('right_index')))
            print("Frame number:", frame_number)
            context['frame_number'] = frame_number

            self.send(
                lyr.Text(t('GUESS', name=name)),
                lyr.Text(get_frame_url(frame_number=frame_number)),
                tl.InlineKeyboard([
                    [tl.InlineKeyboardCallbackButton(
                        text=t.LAUNCHED,
                        payload={
                            'action': 'choose_option',
                            'option': 'launched'
                        }
                    )],
                    [tl.InlineKeyboardCallbackButton(
                        text=t.NOT_LAUNCHED,
                        payload={
                            'action': 'choose_option',
                            'option': 'not_launched'
                        }

                    )]
                ])
            )
        else:
            self.send(
                lyr.Text(t('VIDEO_ERROR')),
            )


class Check_again(RocketLaunchState):
    """
    Checks the answers of the users and decides the next image to show the user modifying the indexes
    Uses the bisection method. This state is where all the next guesses are done.  
    """

    @page_view('/bot/check-again')
    @cs.inject()
    async def handle(self, context) -> None:

        try:
            payload = self.request.get_layer(lyr.Postback).payload
        except KeyError:
            self.send(
                lyr.Text(t('VIDEO_ERROR')),
            )
            return
        else:
            frame_number = context.get('frame_number')
            print('Frame_number:', frame_number)
            option = payload.get('option', 'launched')
            print("Option:", option)

        name = await self.request.user.get_friendly_name()
        # left_index = context.get('left_index')
        # right_index = context.get('right_index')

        # Changing the indexes for the new bisection
        # When the rocket launched
        if option == 'launched':
            print('Launched')
            context['right_index'] = frame_number
            context['left_index'], context['right_index'], new_frame_number = bisect(
                context.get('left_index'), context.get('right_index'))
            context['frame_number'] = new_frame_number
        # When the rocket  not launched
        else:
            print('Not launched')
            context['left_index'] = frame_number
            context['left_index'], context['right_index'], new_frame_number = bisect(
                context.get('left_index'), context.get('right_index'))
            context['frame_number'] = new_frame_number

        self.send(
            lyr.Text(t('GUESS', name=name)),
            lyr.Text(get_frame_url(frame_number=new_frame_number)),
            tl.InlineKeyboard([
                [tl.InlineKeyboardCallbackButton(
                    text=t.LAUNCHED,
                    payload={
                        'action': 'choose_option',
                        'option': 'launched'
                    }
                )],
                [tl.InlineKeyboardCallbackButton(
                    text=t.NOT_LAUNCHED,
                    payload={
                        'action': 'choose_option',
                        'option': 'not_launched'
                    }

                )]
            ])
        )


class Finish(RocketLaunchState):
    """
    Congratulate the user for finding the correct frame and propose to start again
    """
    @page_view('/bot/congrats')
    @cs.inject()
    async def handle(self, context) -> None:
        # name = await self.request.user.get_friendly_name()
        frame_number = context.get('frame_number')
        self.send(
            lyr.Text(t('FINISH', frame_number=frame_number)),
            tl.InlineKeyboard([
                [tl.InlineKeyboardCallbackButton(
                    text=t.PLAY_AGAIN,
                    payload={'action': 'restart'})],
                [tl.InlineKeyboardCallbackButton(
                    text=t.QUIT_PLAY,
                    payload={'action': 'no_restart'})]

            ])
        )


class Quit(RocketLaunchState):
    """
    Skip the conversation, when the user does not want to play for the first time or again after finishing. 
    """
    @page_view('/bot/quit')
    async def handle(self) -> None:
        name = await self.request.user.get_friendly_name()
        self.send(
            lyr.Text(t('GOODBYE', name=name)),
        )
