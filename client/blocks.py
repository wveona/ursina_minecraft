#from ursina import color, raycast
from block_origin import *

class Grass(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "assets/groundEarthCheckered.png"

class Dirt(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "assets/groundMud.png"

class Stone(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "assets/Stone01.png"

class Brick(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "assets/wallBrick01.png"

class Bedrock(Block):
    def __init__(self, position = (0, 0, 0)):
        super().__init__(position)
        self.texture = "assets/stone07.png"
        self.breakable = False
        
block_texture = {
    "grass" : load_texture("assets/groundEarthCheckered.png"),
    "dirt" : load_texture("assets/groundMud.png"),
    "stone" : load_texture("assets/Stone01.png"),
    "brick" : load_texture("assets/wallBrick01.png"),
    "bedrock" : load_texture("assets/stone07.png"),
}