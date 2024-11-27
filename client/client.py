from ursina import *
from ursinanetworking import *
from random import *

App = Ursina()

from block_origin import *
from blocks import *
from player import *

Client = UrsinaNetworkingClient("localhost", 25565)
Easy = EasyUrsinaNetworkingClient(Client)
window.borderless = False

BLOCKS = [
    "grass",
    "dirt",
    "stone",
    "brick",
    "bedrock"
]

block_texture = {
    "grass" : load_texture("assets/groundEarthCheckered.png"),
    "dirt" : load_texture("assets/groundMud.png"),
    "stone" : load_texture("assets/Stone01.png"),
    "brick" : load_texture("assets/wallBrick01.png"),
    "bedrock" : load_texture("assets/stone07.png"),
}

Blocks = {}
Players = {}
PlayersTargetPos = {}

Ply = Player()
INDEX = 1
SELECTED_BLOCK = "grass"
SelfId = -1

@Client.event
def GetId(Id):
    global SelfId
    SelfId = Id
    print(f"My ID is : {SelfId}")

@Easy.event
def onReplicatedVariableCreated(variable):
    global Client
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "block":
        block_type = variable.content["block_type"]
        if block_type == "grass": new_block = Grass()
        elif block_type == "dirt": new_block = Dirt()
        elif block_type == "stone": new_block = Stone()
        elif block_type == "brick": new_block = Brick()
        elif block_type == "bedrock": new_block = Bedrock()
        else:
            print("Block not found.")
            return

        new_block.name = variable_name
        new_block.position = variable.content["position"]
        new_block.client = Client
        Blocks[variable_name] = new_block
    elif variable_type == "player":
        PlayersTargetPos[variable_name] = Vec3(0, 0, 0)
        Players[variable_name] = PlayerRepresentation()
        if SelfId == int(variable.content["id"]):
            Players[variable_name].color = color.red
            Players[variable_name].visible = False

@Easy.event
def onReplicatedVariableUpdated(variable):
    PlayersTargetPos[variable.name] = variable.content["position"]

@Easy.event
def onReplicatedVariableRemoved(variable):
    variable_name = variable.name
    variable_type = variable.content["type"]
    if variable_type == "block":

        destroy(Blocks[variable_name])
        del Blocks[variable_name]

    elif variable_type == "player":
        destroy(Players[variable_name])
        del Players[variable_name]

def input(key):
    global INDEX, SELECTED_BLOCK

    if key == "right mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)
        E = A.entity
        if E:
            pos = E.position + mouse.normal
            Client.send_message("request_place_block", { "block_type" : SELECTED_BLOCK, "position" : tuple(pos)})

    if key == "left mouse down":
        A = raycast(Ply.position + (0, 2, 0), camera.forward, distance = 6, traverse_target = scene)
        E = A.entity
        if E and E.breakable:
            Client.send_message("request_destroy_block", E.name)

    if key == "1": 
        SELECTED_BLOCK = "grass"
    if key == "2":
        SELECTED_BLOCK = "dirt"
    if key == "3":
        SELECTED_BLOCK = "stone"
    if key == "4":
        SELECTED_BLOCK = "brick"
    if key == "5":
        SELECTED_BLOCK = "bedrock"

    if key == "escape": 
        quit() 
    
    Client.send_message("MyPosition", tuple(Ply.position + (0, 1, 0)))

hand_block = Entity( 
    parent = camera,
    model = "assets/block.obj",
    scale = .2, 
    texture = block_texture.get(SELECTED_BLOCK),
    position = (.35, -.25, .5), 
    rotation = (-15, -30, -5) 
)

def update():

    if Ply.position[1] < -5:
        Ply.position = (randrange(0, 15), 10, randrange(0, 15))

    for p in Players:
        try:
            Players[p].position += (Vec3(PlayersTargetPos[p]) - Players[p].position) / 25
        except Exception as e: print(e)
    
    Easy.process_net_events()

    hand_block.texture = block_texture.get(SELECTED_BLOCK)

sky = Sky(texture = "sky_sunset") 

App.run()