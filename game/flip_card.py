from model.model import SIZE, MODEL, RESOURCES
import spyral
from spyral import Image, Animation, DelayAnimation, easing
from fractions import renderInteger

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class FlipCardForm(spyral.Form):
    back = spyral.widgets.Button("Back")
    
class Card(spyral.Sprite):
    PADDING = (20, 30)
    def __init__(self, parent, value=0, index=0, orientation='up', siblings=0):
        spyral.Sprite.__init__(self, parent)
        self.anchor = 'center'
        self._hovered = False
        self.orientation = orientation
        self.value = value
        self.resting_x, self.resting_y = SIZE
        if orientation == 'up':
            self.resting_x *= (index+1.) / (siblings+1)
            self.resting_y *= .666
        elif orientation == 'down':
            self.resting_x *= (index+1.) / (siblings+1)
            self.resting_y *= .333
        self.index = index
        self.reset_offscreen()
        self.enter()
        
        spyral.event.register("input.mouse.down", self.reset_resting)
        spyral.event.register("input.mouse.motion", self.check_hover)
        
    def check_hover(self, pos):
        self.hovered = self.collide_point(pos)
        
    def reset_resting(self, pos):
        if self.collide_point(pos):
            self.stop_all_animations()
            self.x = self.resting_x
            self.y = self.resting_y
        
    def _get_value(self):
        return self._value
        
    def _set_value(self, value):
        self._value = value
        self._render()
        
    def _get_hovered(self):
        return self._hovered
    
    def _set_hovered(self, value):
        if self._hovered != value:
            self._hovered= value
            self._render()
        
    value = property(_get_value, _set_value)
    hovered = property(_get_hovered, _set_hovered)
    
    def reset_offscreen(self):
        self.x = self.resting_x
        if self.orientation == 'up':
            self.y = SIZE[1] + self.height/2
        elif self.orientation == 'down':
            self.y = - self.height/2
        
    def _render(self):
        secondary, primary = (WHITE, BLACK) if self._hovered else (BLACK, WHITE)
        text_color = RED if self.orientation == 'up' else BLUE
        text = renderInteger(self._value, color=text_color)
        self.image = Image(size=text.size + Card.PADDING).fill(primary)
        self.image.draw_rect(secondary, (0,0), self.image.size - (1,1), 2, 'center')
        self.image.draw_image(text, anchor='center')
    
    def enter(self):
        animation = Animation('y', easing.QuadraticOut(self.y, self.resting_y), duration = 1.5)
        animation &= Animation('x', easing.Sine(-64), shift= self.x, duration=1.5)
        self.animate(DelayAnimation(.25 * self.index) + animation)
        
    def smacked(self):
        self.rotation = -45
        animation = Animation('y', easing.


class FlipCard(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(filename="images/castle/castle2.jpg").scale(SIZE)
        
        self.state = 'dealing'
        # 'dealing'
        # 'p1_thinking'
        # 'playing'
        # 'redealing'
        
        flipcard_buttons = FlipCardForm(self)
        flipcard_buttons.back.pos = 200, 100
        
        p1_values = (100, 33, 47, 24, 55)
        p2_values = (35,)
        self.p1_hand = [Card(self, v, i, siblings=len(p1_values), orientation='up') for i, v in enumerate(p1_values)]
        self.p2_hand = [Card(self, v, i, siblings=len(p2_values), orientation='down') for i, v in enumerate(p2_values)]
        
        spyral.event.register("system.quit", spyral.director.quit)
        spyral.event.register("form.FlipCardForm.back.clicked", spyral.director.pop)
        
