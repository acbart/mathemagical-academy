from collections import defaultdict
from spyral import Font

SIZE = WIDTH, HEIGHT = 1200, 900
RESOURCES = defaultdict(dict)
MODEL = {"gender": "male"}


def load_resources():
    RESOURCES["fonts"] = {"math_big": Font("fonts/Nehama.ttf", 100),
                          "math_small": Font("fonts/Nehama.ttf", 80)}