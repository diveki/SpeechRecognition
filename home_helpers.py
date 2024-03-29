from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
import time
from subprocess import call, getoutput
import moc
import gpiozero as gp0
import speech_recognition as sr


speech_topic = {
    'light': ['switch the blue light on', 'turn the green light off', 'make dark', 'give me light', 'lights up', 'leds down', 'switch the red led off', 'turn the yellow diode on', 'turn the led up', 'make the white lights blink', 'blink the leds', 'turn the bulb up', 'switch the bulb off'],
    'music': ['play music', 'play a something', 'start the next song', 'play my favorite song', 'stop playing music', 'play a song', 'play the next music', 'play the next song', 'what is the title of this song', 'who is the singer of this song', 'who is the singer', 'stop the music', 'what band is this', 'which singer is this'],
    'weather': ['what is the weather today', 'is it wet outside', 'how is the weather', 'weather please', 'is it cold outside', 'what it feels like outside', 'what is the temperature', 'is it warm outside', 'what is the temperature outside', 'is it raining', 'is it windy outside', 'is it snowing', 'give me a weather forecast']
}

colour_defs = ['all', 'some', 'red', 'blue', 'green', 'yellow', 'white', 'black', 'orange', 'purple', 'pink', 'cyan', 'brown']
city_names = ['szeged', 'budapest', 'debrecen', 'pecs', 'london', 'paris', 'new york', 'madrid', 'belgrade', 'wien', 'stockholm', 'coppenhagen', 'berlin']
dates = ['today', 'now', 'tomorrow', 'currently']
music_words = ['play', 'next', 'previous', 'stop', 'title', 'name', 'artist', 'singer', 'presenter']

topics_name = [topic for topic in speech_topic.keys() for i in speech_topic[topic]]
topics_features = [i for topic in speech_topic.keys() for i in speech_topic[topic]]


def test_any_membership(text, test):
    tmp = any(i in text for i in test)
    return tmp

def test_all_membership(text, test):
    tmp = all(i in text for i in test)
    return tmp

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


# Create a class to verify if the user wants to quit
class QuitClass:
    def __init__(self):
        self.initialize_options()

    def initialize_options(self):
        self.quit_words = set(['quit', 'exit', 'shut down', 'bye', 'good night', 'good bye'])

    def verify(self, text):
        return test_any_membership(text, self.quit_words)


# Class for controlling music
class MusicPlayer:
    def __init__(self, path):
        self.path = path
        call(['mocp', '-S'])

    def play(self):
        moc.find_and_play(self.path + '/*')

    def next_song(self):
        moc.next()
        #call(['mocp','--next'])

    def previous_song(self):
        #call(['mocp','--previous'])
        moc.previous()

    def stop(self):
        call(['mocp','-s'])

    def _get_info(self):
        out = getoutput('mocp -i')
        out = out.splitlines()
        cont = [line.split(':') for line in out]
        self.song_details = {item[0]:item[1] for item in cont}

    def title(self):
        self._get_info()
        if self.song_details['State'] == 'STOP':
            print('There is no music at the moment. Say play music!')
        else:
            if (self.song_details['Title'] == ' ') and (self.song_details['SongTitle'] == ' '):
                print('The song title was not recorded in the file!')
            else:
                print('The file title is {}'.format(self.song_details['Title']))
                print('The song title is {}'.format(self.song_details['SongTitle']))

    def artist(self):
        self._get_info()
        if self.song_details['State'] == 'STOP':
            print('There is no music at the moment. Say play music!')
        else:
            if self.song_details['Artist'] == ' ':
                print('The artist name was not recorded in the file!')
            else:
                print('The artist name is {}'.format(self.song_details['Artist']))


# Class for controlling the lights
class LightControl:
    def __init__(self, pid, color):
        self.pid = pid
        self.color = color
        self.led = gp0.LED(pid)

    def switch_on(self):
        self.led.on()
        print('{} colored led is on'.format(self.color))
	
    def switch_off(self):
        self.led.off()
        print('{} colored led is off'.format(self.color))

    def blink(self):
        self.led.blink()
        print('{} colored led is blinking'.format(self.color))



# Class for mapping speech to action
class SpeechMap:

    def __init__(self, text, lights, music, features = topics_features, target = topics_name, vectorizer = TfidfVectorizer()):
        self.text = text.lower()
        self._topic = target
        self._topic_features = topics_features
        self._topic_vectorizer = vectorizer
        self._topic_set = np.unique(target)
        self._topic_indecies = np.array_split(range(len(target)), len(self._topic_set))
        self.submaps = {
            'light': [self.find_color, self.light_operation, self.light_action],
            'music': [self.music_operation, self.music_action],
            'weather': [self.find_city, self.find_date, self.weather_action],
            'unknown': [self.unkown_action]
        }
        self.lights = lights
        self.music_player = music


    def find_color(self, color = colour_defs):
        words = self.text.split(' ')
        self.chosen_color = list(set(words) & set(color))

    def find_topic(self):
        self._topic_vocabulary = self._topic_vectorizer.fit_transform(self._topic_features)
        text_transform = self._topic_vectorizer.transform([self.text])
        self.topic_corr = np.array([np.corrcoef(text_transform.toarray()[0],i)[0,1] for i in self._topic_vocabulary.toarray()])
        topic_sum = np.array([np.sum(self.topic_corr[i]) for i in self._topic_indecies])
        max_sum = np.amax(topic_sum)
        arg_sum = np.where(topic_sum == max_sum)
        if max_sum < 1.2:
            print('Unknown topic! Please request something about the following topics: {}'.format(self._topic_set))
            return 'unknown'
        else:
            return self._topic_set[arg_sum][0]

    def allocate_task(self, topic):
        task_list = self.submaps.get(topic)
        for func in task_list:
            func()

    def light_operation(self):
        words = self.text.split(' ')
        tmp = set(words) & set(['on', 'off', 'blink', 'blinking', 'up', 'down', 'dark'])
        if tmp == set():
            self.chosen_operation = []
        else:
            self.chosen_operation = list(tmp)[0]

    def light_action(self):
        if self.chosen_color == []:
            print('Please choose a color!')
            leds = []
        elif self.chosen_color == ['some']:
            leds = self.lights[:1]
        elif self.chosen_color == ['all']:
            leds = self.lights
        else:
            leds = [led for led in self.lights if led.color in self.chosen_color]
            if leds == []:
                print('Please choose a color that exists')
        # select operation
        if self.chosen_operation == []:
            print('Say if you want the lights on, off or blinking!')
        if self.chosen_operation in ['on', 'up']:
            for led in leds:
                led.switch_on()
        if self.chosen_operation in ['blink', 'blinking']:
            for led in leds:
                led.blink()
        if self.chosen_operation in ['off', 'down', 'dark']:
            for led in leds:
                led.switch_off()
        self.chosen_operation = []

    def unkown_action(self):
        print('Please say your instructions again on a different topic!')

    def music_action(self, key_words=music_words):
        words = self.text.split(' ')
        music_words = ['play', 'next', 'previous', 'stop', 'title', 'name', 'artist', 'singer', 'presenter']
        if self.chosen_operation == []:
            print('Say if you want to play, stop, music or want the next, previous song!')
        if self.chosen_operation in ['play']:
            self.music_player.play()
        if self.chosen_operation in ['next']:
            self.music_player.next_song()
        if self.chosen_operation in ['previous']:
            self.music_player.previous_song()
        if self.chosen_operation in ['stop']:
            self.music_player.stop()
        if self.chosen_operation in ['title']:
            self.music_player.title()
        if self.chosen_operation in ['name', 'artist', 'singer', 'presenter', 'band']:
            self.music_player.artist()
        self.chosen_operation = []

    def music_operation(self, key_words=music_words):
        words = self.text.split(' ')
        tmp = set(words) & set(key_words)
        if tmp == set():
            self.chosen_operation = []
        else:
            self.chosen_operation = list(tmp)[0]

    def find_city(self, cities = city_names):
        words = self.text.split(' ')
        self.chosen_city = list(set(words) & set(cities))
        if self.chosen_city == []:
            print('No city found so we set Szeged as the target city!')
            self.chosen_city = ['Szeged']


    def find_date(self, date_options = dates):
        words = self.text.split(' ')
        self.chosen_date = list(set(words) & set(date_options))
        if self.chosen_date == []:
            self.chosen_date = ['now']

    def weather_action(self):
        if self.chosen_date[0] in ['now', 'currently']:
            url = 'wttr.in/' + self.chosen_city[0] + '?0'
        elif self.chosen_date[0] in ['tomorrow']:
            url = 'wttr.in/' + self.chosen_city[0] + '?2'
        elif self.chosen_date[0] in ['today']:
            url = 'wttr.in/' + self.chosen_city[0] + '?1'
        call(['curl', url])

if __name__ == '__main__':
    music_path = './Music'
    music_player = MusicPlayer(music_path)

    led1 = LightControl(1, 'red')
    led2 = LightControl(2, 'blue')
    led3 = LightControl(3, 'green')
    leds = [led1, led2, led3]

    sp=SpeechMap('My name is zsolt', leds, music_player)
    topic = sp.find_topic()
    sp.allocate_task(topic)
