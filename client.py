from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursinanetworking import *

App = Ursina()
Client = UrsinaNetworkingClient("localhost", 25565)

player = FirstPersonController(
    mouse_sensitivity = Vec2(100, 100),
    position = (0, 5, 0)
)

App.run()