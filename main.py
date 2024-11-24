from ursina import *
from ursinanetworking import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import basic_lighting_shader
from perlin_noise import PerlinNoise
import random

Client = UrsinaNetworkingClient("localhost", 25565)


    

    

noise = PerlinNoise(octaves = 3, seed = random.randint(1, 1000)) #랜덤 지형을 위한 노이즈 생성

app = Ursina() #윈도우 생성

selected_block = "grass" #선택된 블럭을 "grass"로 지정

player = FirstPersonController(
    mouse_sensitivity = Vec2(100, 100),
    position = (0, 5, 0)
) #플레이어 설정, 마우스 감도와 초기 위치 지정

block_texture = {
    "grass" : load_texture("assets/groundEarthCheckered.png"),
    "dirt" : load_texture("assets/groundMud.png"),
    "stone" : load_texture("assets/Stone01.png"),
    "brick" : load_texture("assets/wallBrick01.png"),
    "bedrock" : load_texture("assets/stone07.png"),
}   #assets 폴더에 있는 이미지들을 로드하며 딕셔너리형으로 저장

def input(key): #키 입력 함수를 선언
    global selected_block   #"selected_block"을 전역변수로 선언

    if key == "right mouse down": #만약 오른쪽 마우스가 클릭되면
        hit_info = raycast(camera.world_position, camera.forward, distance = 10) 
        #거리가 10 까지 카메라 포인트에 감지된 엔티티를 "hit_info"에 저장

        if hit_info.hit: #만약 "hit_info"에 감지된 엔티티가 히트되면
            block = Block(hit_info.entity.position + hit_info.normal, selected_block )
            #그 자리에 블럭설치

    if key == "left mouse down" and mouse.hovered_entity: #만약 오른쪽 마우스를 클릭하고 마우스 위치에 엔티티가 있으면
        if not mouse.hovered_entity.block_type == "bedrock": #만약 마우스 위치에 있는 엔티티의 "block_type" 이 "bedrock"이 아니면
            destroy(mouse.hovered_entity) #마우스 위치에 있는 엔티티를 삭제

    
    if key == "1": #만약 1에서 5까지의 버튼중 하나를 누르면 "selected_block"을 변경
        selected_block = "grass"
    if key == "2":
        selected_block = "dirt"
    if key == "3":
        selected_block = "stone"
    if key == "4":
        selected_block = "brick"
    if key == "5":
        selected_block = "bedrock"

    
    if key == "escape": #만약 esc를 누른다면
        quit() #게임 종료


BLOCKS_PARENT = Entity()

class Block(Button): #"Entity"클래스를 상속받는 "Block" 클래스를 선언
    def __init__(self, position, block_type): #매개변수가 "position", "block_type"인 생성자 선언
        super().__init__( #"Entity"의 메소드를 불러옴
            parent = BLOCKS_PARENT,
            position = position,
            model = "assets/block.obj", #엔티티의 모델을 assets 폴더의 "block.obj" 로  저장
            scale = 1, #엔티티의 스케일을 1 로 저장
            origin_y = -.5, #엔티티의 초기 y좌표를 -0.5로 저장
            texture = block_texture.get(block_type), 
            #엔티티의 텍스쳐를 "block_texture" 딕셔너리의 "block_type"키의 밸류로 저장
            collider = "box", #엔티티에 박스모양 충돌판정을 저장
            shader = basic_lighting_shader,
            color = color.white,
        )
        self.block_type = block_type

hand_block = Entity( #"hand_block" 을 엔티티 함수로 저장
    parent = camera, #부모속성을 카메라로 지정
    model = "assets/block.obj", #엔티티의 모델을 assets 폴더의 "block.obj" 로  저장
    scale = .2, #엔티티의 스케일을 0.2 로 저장
    texture = block_texture.get(selected_block),
    #엔티티의 텍스쳐를 "block_texture" 딕셔너리의 "block_type"키의 밸류로 저장
    position = (.35, -.25, .5), #엔티티의 위치를 x:0.35, y:-0.25, z:0.5로 지정
    rotation = (-15, -30, -5) #엔티티의 회전값을 x:-15, y:-30, z:-5 로 지정
)

min_height = -4 #월드 생성의 최소 높이를 -4로 지정

for x in range(-7, 7): #변수 x의 반복문을 -10 부터 10까지 반복
    for z in range(-7, 7): #변수 z의 반복문을 -10 부터 10까지 반복
        height = noise([x * .02, z * .02]) #"noise"
        height = math.floor(height * 7.5) #"height" x 7.5를 내림하여 다시 "height"에 저장

        for y in range(height, min_height - 1, -1): 
            #변수 y의 반복문을 "height" 부터 "min_height - 1"의 간격으로 -1 까지 반복

            if y == min_height: #만약 y가 "min_height"와 같다면 
                block = Block((x, y + min_height, z), "bedrock") 
                #x, y + min_height, z 좌표에 텍스쳐가 "bedrock"인 블록 생성

            elif y == height: #만약 y 가 "height"와 같다면
                block = Block((x, y + min_height, z), "grass")
                 #x, y + min_height, z 좌표에 텍스쳐가 "grass"인 블록 생성

            elif height - y > 2: #만약 "height - y"가 2보다 크다면 
                block = Block((x, y + min_height, z), "stone")
                 #x, y + min_height, z 좌표에 텍스쳐가 "stone"인 블록 생성

            else: #아니라면
                block = Block((x, y + min_height, z), "dirt")
                 #x, y + min_height, z 좌표에 텍스쳐가 "dirt"인 블록 생성

def update(): #"update"함수 선언, 이함수는 게임 실행중 자동으로 무한 반복하여 실행됨
    hand_block.texture = block_texture.get(selected_block) 
    #"hand_block"의 "texture"를 "block_texture" 딕셔너리의 "block_type"키의 밸류로 저장

    if held_keys["left mouse"] or held_keys["right mouse"]: 
        #만약 왼쪽 마우스키 또는 오른쪽 마우스키가 눌렸다면
        hand_block.position = (.35, -.25, .6) #"hand_block"의 "position"을 0.35, -0.25, 0.6으로 지정
    else: #아니라면
        hand_block.position = (.35, -.25, .5) #"hand_block"의 "position"을 0.35, -0.25, 0.5으로 지정

    if player.y <= -30: #만약 플레이어의 y좌표가 -30보다 작다면
        player.position = (0, 5, 0) #플레이어의 조표를 0, 5, 0 으로 설정

    Client.process_net_events()

sky = Sky(texture = "sky_sunset") 
#텍스쳐가 "sky_sunset"인 "Sky"함수를 sky에 저장, 게임에서의 하늘 텍스쳐가 됨(이 함수의 "sky_sunset"텍스쳐는 ursina 엔진에 내장된 텍스쳐임)

@Client.event
def HelloFromServer():
    block = Block((0, 5, 0), "bedrock")


app.run() #게임 실핼


