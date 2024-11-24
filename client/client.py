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


App.run()