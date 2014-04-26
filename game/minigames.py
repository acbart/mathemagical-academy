from model.model import SIZE, MODEL, RESOURCES
from flip_card import FlipCard
import spyral

class MinigameForm(spyral.Form):
    flip_card = spyral.widgets.Button("Flip Card")
    back = spyral.widgets.Button("Back")


class MiniGames(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(filename="images/castle/castle1.jpg").scale(SIZE)
        
        minigame_buttons = MinigameForm(self)
        minigame_buttons.flip_card.pos = 200, 500
        minigame_buttons.back.pos = 200, 550
        
        spyral.event.register("system.quit", spyral.director.quit)
        spyral.event.register("form.MinigameForm.back.clicked", spyral.director.pop)
        spyral.event.register("form.MinigameForm.flip_card.clicked", lambda : spyral.director.push(FlipCard()))