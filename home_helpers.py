
speech_topic = [('switch the light on', 'light'), ('turn the light off','light'), ('make dark', 'light'), ('give me light','light'), ('lights up','light'), ('leds down','light'), ('switch the red led off','light'), ('turn the diode on','light'), ('let there be light','light'), ('make the lights blink','light'), ('blink the leds','light'), ('turn the bulb up','light'), ('switch the bulb off','light'),
    ('play music','music'), ('play a something','music'), ('start the next song','music'), ('play my favorite song','music'), ('stop playing music','music'), ('play a song','music'), ('play the next music','music'), ('play the next song','music'), ('what is the title of this song','music'), ('who is the singer of this song','music'), ('stop the music','music'), ('what band is this','music'), ('which singer is this','music'),
    ('what is the weather today','weather'), ('is it wet outside','weather'), ('how is the weather','weather'), ('weather please','weather'), ('is it cold outside','weather'), ('what it feels like outside','weather'), ('what is the temperature','weather'), ('is it warm outside','weather'), ('what is the temperature outside','weather'), ('is it raining','weather'), ('is it windy outside','weather'), ('is it snowing','weather'), ('give me a weather forecast','weather')]


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
