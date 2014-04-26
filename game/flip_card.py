from model.model import SIZE, MODEL, RESOURCES
import spyral
from spyral import Image, Animation, DelayAnimation, easing
from fractions import renderInteger

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class FlipCardForm(spyral.Form):
    back = spyral.widgets.Button("Back")
    
class Card(spyral.Sprite):
    PADDING = (20, 30)
    def __init__(self, parent, value=0, index=0):
        spyral.Sprite.__init__(self, parent)
        self.anchor = 'center'
        self.value = value
        self.resting_x, self.resting_y = 0,0
        self.index = index
        
        spyral.event.register("input.mouse.down", self.reset_resting)
        
    def reset_resting(self, pos):
        if (self.collide_point(pos)):
            self.stop_all_animations()
            self.x = self.resting_x
            self.y = self.resting_y
        
    def _get_value(self):
        return self._value
    def _set_value(self, value):
        self._value = value
        self._render()
    value = property(_get_value, _set_value)
    
    def reset_offscreen(self):
        self.x = self.resting_x
        self.y = SIZE[1] + self.height/2
        
    def _render(self):
        text = renderInteger(self._value)
        self.image = Image(size=text.size + Card.PADDING).fill(WHITE)
        self.image.draw_rect(BLACK, (0,0), self.image.size, 2, 'center')
        self.image.draw_image(text, anchor='center')
    
    def enter(self):
        animation = Animation('y', easing.QuadraticOut(self.y, self.resting_y), duration = 1.5)
        animation &= Animation('x', easing.Sine(-64), shift= self.x, duration=1.5)
        self.animate(DelayAnimation(.25 * self.index) + animation)


class FlipCard(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(filename="images/castle/castle2.jpg").scale(SIZE)
        
        flipcard_buttons = FlipCardForm(self)
        flipcard_buttons.back.pos = 200, 100
        
        self.p1_hand = [Card(self, v, i) for i, v in enumerate((100, 33, 47, 24, 55))]
        for i, card in enumerate(self.p1_hand):
            card.resting_x = (i+1) * SIZE[0] / (len(self.p1_hand)+1)
            card.resting_y = SIZE[1] * .666
            card.reset_offscreen()
            card.enter()
        
        spyral.event.register("system.quit", spyral.director.quit)
        spyral.event.register("form.FlipCardForm.back.clicked", spyral.director.pop)
        
