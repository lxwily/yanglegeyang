import struct
import base64
import time
import requests
import os
token =  input('请输入你的token: ')
total =  input('请输入闯关次数: ')
os.environ['NO_PROXY'] = "https://cat-match.easygame2021.com"
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'Connection': 'keep-alive',
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/16/page-frame.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/4629 MicroMessenger/8.0.27.2220(0x28001B37) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    't': token
}

url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
r = requests.get(url, headers=headers)
print('获取当前闯关',r.json()['data']['win_count'])
for i in range(int(total)):
    url = 'https://cat-match.easygame2021.com/sheep/v1/game/map_info_ex?matchType=3'
    r2 = requests.get(url, headers=headers)
    map_md5 = r2.json()['data']['map_md5'][1]
    url = f'https://cat-match-static.easygame2021.com/maps/{map_md5}.txt'  # 由于每天获取的地图不一样，需要计算地图大小
    r = requests.get(url)
    levelData = r.json()['levelData']
    p = []
    for h in range(len(sum(levelData.values(), []))):  # 生成操作序列
        p.append({'chessIndex': 127 if h > 127 else h, 'timeTag': 127 if h > 127 else h})
    GAME_DAILY = 3
    data = struct.pack('BB', 8, GAME_DAILY)
    for i in p:
        c, t = i.values()
        data += struct.pack('BBBBBB', 34, 4, 8, c, 16, t)
    matchPlayInfo = base64.b64encode(data).decode('utf-8')
    for i in range(60):
        time.sleep(1)
        print('等待完成{}秒'.format(int(60 - i)))
    url = 'https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex?t={}'.format(token)
    r = requests.post(url, headers=headers,
                      json={'rank_score': 1, 'rank_state': 1, 'rank_time': 359, 'rank_role': 2, 'skin': 1,
                            'MatchPlayInfo': matchPlayInfo})
    print('闯关记录', r.text)
    url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
    r = requests.get(url, headers=headers)
    print('获取最新闯关', r.json()['data']['win_count'])