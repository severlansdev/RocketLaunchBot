# import libraries
import io
import os
from typing import List, NamedTuple, Text
from urllib.parse import quote, urljoin
import json
import requests

# get the variables for the video 
from .environment import API_URL, VIDEO_NAME

# The following methods are useful for obtaining the information related to the video and the frames for the development. 

def get_video_url():
    """
     Get the url for the specific video and fethes information about a video
    """
    return f'{API_URL}{quote(VIDEO_NAME)}'

def get_video_information():
    """
     Reads the information about the video and returns the total_frames
    """
    url = get_video_url()
    response = requests.get(url)
    info =response.json()
    number_frames = info['frames']
    return number_frames

def get_frame_url(frame_number:int):
    """
     Get the url for an specific framework  by giving the frame number desired. 
    """
    return f'{get_video_url()}/frame/{frame_number}'











