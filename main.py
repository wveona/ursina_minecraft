from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random

noise = PerlinNoise(octaves = 3, seed = random.randint(1, 1000))

app = Ursina()

selected_block = "grass"

player = FirstPersonController(
    mouse_sensitivity = Vec2(100, 100),
    position = (0, 5, 0)
)

block_texture = {
    "grass" : load_texture("assets/groundEarthCheckered.png"),
    "dirt" : load_texture("assets/groundMud.png"),
    "stone" : load_texture("assets/Stone01.png"),
    "brick" : load_texture("assets/wallBrick01.png"),
    "bedrock" : load_texture("assets/stone07.png"),
}

def input(key):
    global selected_block

    if key == "right mouse down":
        hit_info = raycast(camera.world_position, camera.forward, distance = 10)
        if hit_info.hit:
            block = Block(hit_info.entity.position + hit_info.normal, selected_block )

    if key == "left mouse down" and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            destroy(mouse.hovered_entity)

    if key == "1":
        selected_block = "grass"
    if key == "2":
        selected_block = "dirt"
    if key == "3":
        selected_block = "stone"
    if key == "4":
        selected_block = "brick"
    if key == "5":
        selected_block = "bedrock"

    if key == "escape":
        quit()



class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position = position,
            model = "assets/block.obj",
            scale = 1,
            origin_y = -.5,
            texture = block_texture.get(block_type),
            collider = "box"
        )
        self.block_type = block_type

hand_block = Entity(
    parent = camera,
    model = "assets/block.obj",
    scale = .2,
    texture = block_texture.get(selected_block),
    position = (.35, -.25, .5),
    rotation = (-15, -30, -5)
)

min_height = -4

for x in range(-10, 10):
    for z in range(-10, 10):
        height = noise([x * .02, z * .02])
        height = math.floor(height * 7.5)
        for y in range(height, min_height - 1, -1):
            if y == min_height:
                block = Block((x, y + min_height, z), "bedrock")
            elif y == height:
                block = Block((x, y + min_height, z), "grass")
            elif height - y > 2:
                block = Block((x, y + min_height, z), "stone")
            else:
                block = Block((x, y + min_height, z), "dirt")

def update():
    hand_block.texture = block_texture.get(selected_block)

    if held_keys["left mouse"] or held_keys["right mouse"]:
        hand_block.position = (.35, -.25, .6)
    else:
        hand_block.position = (.35, -.25, .5)

sky = Sky(texture = "sky_sunset")
app.run()


