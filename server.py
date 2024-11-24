from ursinanetworking import *
from ursina import *
from perlin_noise import PerlinNoise

Server = UrsinaNetworkingServer("localhost", 25565)
Easy = EasyUrsinaNetworkingServer(Server)
Blocks = {}

def destroy_block(Block_name):
    del Blocks[Block_name]
    Easy.remove_replicated_variable_by_name(Block_name)

i = 0
def spawn_block(block_type, position, investigator = "client"):
    global i
    block_name = f"blocks_{i}"
    Easy.create_replicated_variable(
        block_name,
        { "type" : "block", "block_type" : block_type, "position" : position, "investigator" : investigator}
    )
    
    Blocks[block_name] = {
        "name" : block_name,
        "position" : position
    }
    i += 1

@Server.event
def request_destroy_block(Client, Block_name):
    destroy_block(Block_name)

@Server.event
def request_place_block(Client, Content):
    spawn_block(Content["block_type"], Content["position"])

@Server.event
def MyPosition(Client, NewPos):
    Easy.update_replicated_variable_by_name(f"player_{Client.id}", "position", NewPos)
        
min_height = -4
noise = PerlinNoise(octaves = 3, seed = random.randint(1, 1000))

for x in range(-7, 7): 
    for z in range(-7, 7): 
        height = noise([x * .02, z * .02]) 
        height = math.floor(height * 7.5) 

        for y in range(height, min_height - 1, -1): 

            if y == min_height:  spawn_block("bedrock", (x, y, z), investigator = "server")

            elif y == height: spawn_block("grass", (x, y, z), investigator = "server")

            elif height - y > 2: spawn_block("stone", (x, y, z), investigator = "server")

            else: spawn_block("dirt", (x, y, z), investigator = "server")

while True:
    Easy.process_net_events()


