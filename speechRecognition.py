#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 27 09:43:25 2018

@author: diveki
"""

import random
import time

import speech_recognition as sr
from home_helpers import *


music_path = './Music'
music_player = MusicPlayer(music_path)

led1 = LightControl(1, 'red')
led2 = LightControl(2, 'blue')
led3 = LightControl(3, 'green')
leds = [led1, led2, led3]


rec = sr.Recognizer()
try:
    mic = sr.Microphone()
except:
    pass

quit_state = False
quit_class = QuitClass()

while True:
    input('Press enter and tell me instructions: ')
    try:
        text_object = recognize_speech_from_mic(rec, mic)
        text = text_object['transcription']
    except:
        text = input('I am waiting for your request. Please type it in: \n')
    ##################################
    # Check if the command was to quit
    quit_state = quit_class.verify(text)
    if quit_state:
        break
    ##################################
    # Determine the context topic
    sp=SpeechMap(text, leds, music_player)
    topic = sp.find_topic()
    sp.allocate_task(topic)

    

