import threading
import time
import requests as rs
from mcrcon import MCRcon
import time
from obswebsocket import obsws, requests

server_address = "192.168.2.125"  # 替换为Minecraft服务器的IP地址
server_port = 25575  # 替换为Minecraft服务器RCON端口号
rcon_password = "asd951753"  # 替换为你实际设置的RCON密码
obs_client = obsws("localhost", 4455, "951753")
obs_client.connect()


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
    client = MCRcon(server_address, rcon_password)
    client.connect()

def get_likes(video_id):
    url = f"http://api.bilibili.com/x/web-interface/wbi/view?aid={video_id}"
    try:
        response = rs.get(url)
        data = response.json()
        likes = data['data']['stat']['like']
        return likes
    except:
        pass

def update_likes_on_minecraft_server(likes):

    # 摆放新的数字方块
    x, y, z = x1, y1, z1 = 2069, 81, -2015  # 替换为数字方块的起始位置坐标

    x2 = x1 - 30
    y2 = y1 - 7
    z2 = z1

    # 清空之前的数字方块
    likes = str(likes)
    client.command(f"fill {x1} {y1} {z1} {x2} {y2} {z2} minecraft:air")
    print('更新方块数字:',likes)
    for digit in likes:
        if digit in digit_shapes:
            shape = digit_shapes[digit]
            for i, row in enumerate(shape):
                for j, char in enumerate(row):
                    if char == '#':
                        client.command(f"setblock {x - j} {y - i} {z} minecraft:ochre_froglight")
            x -= 4  # 数字之间的间距

def send_fireball(idx,length):
    if(idx == 0):
        obs_client.call(requests.StartRecord())
    client.command("summon minecraft:fireball 2074 64 -2048 {ExplosionPower:1,Motion:[1.0,0.0,0.0]}")
    if(idx == length - 1):
        threading.Timer(2, lambda: obs_client.call(requests.StopRecord())).start()

connect_to_server(server_address, server_port, rcon_password)
video_id = 387970154  # 替换为你要获取点赞数的视频ID
likes = None
def watch_likes():
    global likes
    while True:
        new_likes = get_likes(video_id)
        print(f"点赞数：{new_likes}, 旧点赞数：{likes}")
        if (new_likes != likes and new_likes != None):
            if(likes != None):
                print(f"触发 {abs(new_likes - likes)} 次")
                update_likes_on_minecraft_server(new_likes)
                for i in range(abs(new_likes - likes)):
                    send_fireball(i,abs(new_likes - likes))
            likes = new_likes
            print('新点赞')
        time.sleep(2)

if __name__ == '__main__':
    watch_likes()
