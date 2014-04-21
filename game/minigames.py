from model import SIZE, MODEL, RESOURCES
import spyral

class MiniGames(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(filename="images/castle/castle1.jpg")
        
        