from spyral import Sprite, Image
from model.model import RESOURCES

def renderInteger(value):
    big_font = RESOURCES["fonts"]["math_big"]
    #small_font = RESOURCES["fonts"]["math_small"]
    return big_font.render(str(value))