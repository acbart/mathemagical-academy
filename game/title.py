from model import SIZE, MODEL, RESOURCES
from minigames import MiniGames
import spyral

class TitleForm(spyral.Form):
    story = spyral.widgets.Button("Story")
    minigames = spyral.widgets.Button("Minigame")
    options = spyral.widgets.Button("Options")
    exit = spyral.widgets.Button("Exit")

class Title(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(filename="images/title.png")
        
        title_buttons = TitleForm(self)
        title_buttons.story.pos = 200, 500
        title_buttons.minigames.pos = 200, 550
        title_buttons.options.pos = 200, 600
        title_buttons.exit.pos = 200, 650
        
        #spyral.event.register("director.update", self.update)
        spyral.event.register("system.quit", spyral.director.quit)
        spyral.event.register("form.TitleForm.minigames.clicked", lambda : spyral.director.push(MiniGames()))
        spyral.event.register("form.TitleForm.exit.clicked", spyral.director.quit)