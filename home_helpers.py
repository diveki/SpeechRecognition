
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