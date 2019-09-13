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


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def switchLed(*arg, **kwargs):
    col = kwargs.get('col')
    state = kwargs.get('state')
    print('switch %s light %s' % (col, state))
    
def test_all_membership(text, test):
    tmp = all(i in text for i in test)
    return tmp

def test_any_membership(text, test):
    tmp = any(i in text for i in test)
    return tmp


def check_state(text, col):
    tmp = set(list(col)) & set(text)
    return list(tmp)

def light_switch_on_speech(text, leds, colors = {'red', 'blue'}, *args, **kwargs):
    text_list = text.lower().split()
    onOff = set(['off', 'on'])
    quitSet = set(['quit', 'exit', 'shut down', 'bye', 'good night'])
    quit_state = test_any_membership(text_list, quitSet)
    if quit_state:
        print('Bye bye')
        return True
    else:
        lit_value = check_state(text_list, onOff)
        color_value = check_state(text_list, colors)
        if all([lit_value, color_value]):
            func = leds.get(color_value[0])
            func(col=color_value[0], state=lit_value[0])
            return False
        else:
            print('You should say `on`, `off` and the color of the light!!')
            return False
    

rec = sr.Recognizer()
mic = sr.Microphone()

leds = {'red': switchLed,
        'blue': switchLed
        }
quit_state = False

quit_class = QuitClass()

while True:
    input('Press enter and tell me instructions: ')
    a = recognize_speech_from_mic(rec, mic)
    text = a['transcription']
    ##################################
    # Check if the command was to quit
    quit_state = quit_class.verify(text)
    # quit_state = light_switch_on_speech(a['transcription'], leds)
    if quit_state:
        break
    ##################################
    # Determine the context topic
    sp = SpeechMap(text)
    topic = sp.find_topic()
    

