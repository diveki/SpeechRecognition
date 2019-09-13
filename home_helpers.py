from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np

speech_topic = {
    'light': ['switch the blue light on', 'turn the green light off', 'make dark', 'give me light', 'lights up', 'leds down', 'switch the red led off', 'turn the yellow diode on', 'let there be light', 'make the white lights blink', 'blink the leds', 'turn the bulb up', 'switch the bulb off'],
    'music': ['play music', 'play a something', 'start the next song', 'play my favorite song', 'stop playing music', 'play a song', 'play the next music', 'play the next song', 'what is the title of this song', 'who is the singer of this song', 'stop the music', 'what band is this', 'which singer is this'],
    'weather': ['what is the weather today', 'is it wet outside', 'how is the weather', 'weather please', 'is it cold outside', 'what it feels like outside', 'what is the temperature', 'is it warm outside', 'what is the temperature outside', 'is it raining', 'is it windy outside', 'is it snowing', 'give me a weather forecast']
}

topics_name = [topic for topic in speech_topic.keys() for i in speech_topic[topic]]
topics_features = [i for topic in speech_topic.keys() for i in speech_topic[topic]]

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
    def __init__(self, text, features = topics_features, target = topics_name, vectorizer = TfidfVectorizer()):
        self.text = text.lower()
        self._topic = target
        self._topic_features = topics_features
        self._topic_vectorizer = vectorizer
        self._topic_set = np.unique(target)
        self._topic_indecies = np.array_split(range(len(target)), len(self._topic_set))        

    def find_color(self):
        pass
    
    def find_topic(self):
        self._topic_vocabulary = self._topic_vectorizer.fit_transform(self._topic_features)
        text_transform = self._topic_vectorizer.transform([self.text])
        # import pdb
        # pdb.set_trace()
        self.topic_corr = np.array([np.corrcoef(text_transform.toarray()[0],i)[0,1] for i in self._topic_vocabulary.toarray()])
        topic_sum = np.array([np.sum(self.topic_corr[i]) for i in self._topic_indecies])
        max_sum = np.amax(topic_sum)
        arg_sum = np.where(topic_sum == max_sum)
        if max_sum < 1.2:
            print('Unkown topic! Please request something about the following topics: {}'.format(self._topic_set))
            return 'unkown'
        else:
            return self._topic_set[arg_sum][0]





