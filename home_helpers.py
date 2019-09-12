
speech_topic = {
    'light': ['switch the light on', 'turn the light off', 'make dark', 'give me light', 'lights up', 'leds down', 'switch the red led off', 'turn the diode on', 'let there be light', 'make the lights blink', 'blink the leds', 'turn the bulb up', 'switch the bulb off'],
    'music': ['play music', 'play a song', 'play the next music', 'play the next song', 'what is the title of this song', 'who is the singer of this song', 'stop the music', 'what band is this', 'which singer is this'],
    'weather': ['what is the weather today', 'what is the temperature outside', 'is it raining', 'is it windy outside', 'is it snowing', 'give me a weather forecast']
}

def test_any_membership(text, test):
    tmp = any(i in text for i in test)
    return tmp

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
    def __init__(self):
        pass
    
    def play(self):
        pass
    
    def next_song(self):
        pass
    
    def stop(self):
        pass
    
    def title(self):
        pass


# Class for controlling the lights
class LightControl:
    def __init__(self, id, color):
        self.id = id
        self.color = color
    
    def switch_on(self):
        pass
    
    def switch_off(self):
        pass
    
    def blink(self):
        pass


# Class for mapping speech to action
class SpeechMap:
    def __init__(self, text):
        self.text = text.lower().split()
    
    def find_color(self):
        pass
