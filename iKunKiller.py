import threading
import time
import requests
import keyboard
from rcon import Client
server_address = "mcadmin.bbrealm.com"  # 替换为Minecraft服务器的IP地址
server_port = 25575  # 替换为Minecraft服务器RCON端口号
rcon_password = "nishisola"  # 替换为你实际设置的RCON密码

# 数字形状定义
digit_shapes = {
    '0': [
        "###",
        "# #",
        "# #",
        "# #",
        "###"
    ],
    '1': [
        "  #",
        "  #",
        "  #",
        "  #",
        "  #"
    ],
    '2': [
        "###",
        "  #",
        "###",
        "#  ",
        "###"
    ],
    '3': [
        "###",
        "  #",
        "###",
        "  #",
        "###"
    ],
    '4': [
        "# #",
        "# #",
        "###",
        "  #",
        "  #"
    ],
    '5': [
        "###",
        "#  ",
        "###",
        "  #",
        "###"
    ],
    '6': [
        "###",
        "#  ",
        "###",
        "# #",
        "###"
    ],
    '7': [
        "###",
        "  #",
        "  #",
        "  #",
        "  #"
    ],
    '8': [
        "###",
        "# #",
        "###",
        "# #",
        "###"
    ],
    '9': [
        "###",
        "# #",
        "###",
        "  #",
        "###"
    ]
}

client = None

def connect_to_server(server_address, server_port, rcon_password):
    global client
    client = Client(server_address, server_port, rcon_password)

def get_likes(video_id):
    url = f"https://api.bilibili.com/x/web-interface/wbi/view?aid={video_id}"
    response = requests.get(url)
    data = response.json()
    likes = data['data']['stat']['like']
    return likes

def update_likes_on_minecraft_server(likes):
    # 清空之前的数字方块
    likes = int(likes)
    client.run(f"/fill {x1} {y1} {z1} {x2} {y2} {z2} minecraft:air")

    # 摆放新的数字方块
    x, y, z = x1, y1, z1 = 100, 64, 100  # 替换为数字方块的起始位置坐标

    x2 = x1 + 10
    y2 = y1 + 10
    z2 = z1

    for digit in likes:
        if digit in digit_shapes:
            shape = digit_shapes[digit]
            for i, row in enumerate(shape):
                for j, char in enumerate(row):
                    if char == '#':
                        client.run(f"/setblock {x + j} {y + i} {z} minecraft:stone")
            x += 4  # 数字之间的间距

def send_fireball(idx,length):
    if(idx == 0):
        keyboard.press('F8')
    client.run("/summon minecraft:fireball ~ ~1 ~ {ExplosionPower:100,direction:[0.0,0.0,0.0]}")
    if(idx == length - 1):
        threading.Timer(2, lambda: keyboard.press('F8')).start()

#connect_to_server(server_address, server_port, rcon_password)
video_id = 857470696  # 替换为你要获取点赞数的视频ID
likes = None
def watch_likes():
    global likes
    while True:
        new_likes = get_likes(video_id)
        print(f"点赞数：{new_likes}, 旧点赞数：{likes}")
        if (new_likes != likes):
            if(likes != None):
                print(f"触发 {abs(new_likes - likes)} 次")
                update_likes_on_minecraft_server(likes)
                for i in range(abs(new_likes - likes)):
                    send_fireball(i,abs(range(new_likes - likes)))
            likes = new_likes
            print('新点赞')
        time.sleep(1)

if __name__ == '__main__':
    for i in range(1):
        print(i)
    #watch_likes()
