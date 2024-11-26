from ursina import *
from ursina.shaders import basic_lighting_shader

BLOCKS_PARENT = Entity()

class Block(Button): 
    def __init__(self, position = (0, 0, 0)): 
        super().__init__( 
            parent = BLOCKS_PARENT,
            position = position,
            model = "assets/block.obj",
            scale = 1, 
            origin_y = .5, 
            collider = "box", 
            shader = basic_lighting_shader,
            color = color.white,
        )
        self.name = "unnamed_block"
        self.client = None
        self.breakable = True