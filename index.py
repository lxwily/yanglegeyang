import struct
import base64
import requests

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,compress,br,deflate',
    'Connection': 'keep-alive',
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/16/page-frame.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4313 MMWEBSDK/20220805 Mobile Safari/537.36 MMWEBID/4629 MicroMessenger/8.0.27.2220(0x28001B37) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
    't': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTQyMzc5MDEsIm5iZiI6MTY2MzEzNTcwMSwiaWF0IjoxNjYzMTMzOTAxLCJqdGkiOiJDTTpjYXRfbWF0Y2g6bHQxMjM0NTYiLCJvcGVuX2lkIjoiIiwidWlkIjoyMTY3NTU2MCwiZGVidWciOiIiLCJsYW5nIjoiIn0.lUQOMRm8vI4W4J2Tru021GFG834hss8K-G1d9kWPfRA'
}

url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
r = requests.get(url, headers=headers)
print('更新个人资料',r.text)
url = 'https://cat-match.easygame2021.com/sheep/v1/game/map_info_ex?matchType=3'
r2 = requests.get(url, headers=headers)
print('获取MD5',r2.text)
map_md5 = r2.json()['data']['map_md5'][1]
url = f'https://cat-match-static.easygame2021.com/maps/{map_md5}.txt'  # 由于每天获取的地图不一样，需要计算地图大小
r = requests.get(url)
levelData = r.json()['levelData']
p = []
for h in range(len(sum(levelData.values(), []))):  # 生成操作序列
    p.append({'chessIndex': 127 if h > 127 else h, 'timeTag': 127 if h > 127 else h})
GAME_DAILY = 3
GAME_TOPIC = 4
data = struct.pack('BB', 8, GAME_DAILY)
for i in p:
    c, t = i.values()
    data += struct.pack('BBBBBB', 34, 4, 8, c, 16, t)
MatchPlayInfo = base64.b64encode(data)
print('获取MatchPlayInfo',MatchPlayInfo)
url = 'https://cat-match.easygame2021.com/sheep/v1/game/game_over_ex?'
r = requests.post(url, headers=headers,
                  json={'rank_score': 1, 'rank_state': 1, 'rank_time': 1, 'rank_role': 1, 'skin': 1,
                        'MatchPlayInfo': str(MatchPlayInfo)})
print('闯关记录',r.text)
url = 'https://cat-match.easygame2021.com/sheep/v1/game/personal_info?'
r = requests.get(url, headers=headers)
print('再次更新数据',r.text)
