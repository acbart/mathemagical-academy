import sys
import gtk
import pygame
import os
import sugar.activity.activity
import sugar.graphics.toolbutton

sys.path.insert(0, os.path.abspath("libraries"))
import sugargame
import sugargame.canvas
import spyral

class Activity(sugar.activity.activity.Activity):
    def __init__(self, handle):
        super(Activity, self).__init__(handle)
        self.paused = False
        
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        self.set_canvas(self._pygamecanvas)
        
        def run():
            spyral.director.init((1200,900), fullscreen = False, max_fps = 30)
            game.main()
            spyral.director.run(sugar = True)
            
        self._pygamecanvas.run_pygame(run)

    def read_file(self, file_path):
        pass

    def write_file(self, file_path):
        pass


def main():
    spyral.director.init((0,0), fullscreen = False, max_fps = 30)
    import game
    game.main()
    try:
        spyral.director.run()
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == '__main__':
    main()