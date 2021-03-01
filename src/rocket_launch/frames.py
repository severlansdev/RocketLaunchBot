import io
import os
from typing import List, NamedTuple, Text
from urllib.parse import quote, urljoin
import json
import requests

# import pygame
# from httpx import Client
# from PIL import Image
# from PyInquirer import prompt

from .environment import API_URL, VIDEO_NAME 

def get_video_url():
    """
     Get the url for the specific video and fethes information about a video
    """
    return f'{API_URL}{quote(VIDEO_NAME)}'


def get_total_frames():
    """
     Returns the total frames in the video
    """
def get_video_information():
    """
     Reads the information about the video and returns the total_frames
    """
    url = get_video_url()
    response = requests.get(url)
    info =response.json()
    number_frames = info['frames']
    # print("Frames:", number_frames)
    return number_frames

def get_frame_url(frame_number:int):
    """
     Get the url for an specific framework
    """
    return f'{get_video_url()}/frame/{frame_number}'











