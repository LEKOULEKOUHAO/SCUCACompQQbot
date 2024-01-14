from nonebot.adapters.onebot.v11 import MessageSegment
import os

from .utils import create_table, response
from .data_source import _font_path, url_scuca

url_score = f'{url_scuca}competition/week/score/' #积分榜
url_uestc = f'{url_scuca}rank/score/' #沉淀值榜

#积分数据，若本周还没有返回0
def response_score():
    r = response(url_score)
    if(r):
        return r
    else:
        return 0

#score的展示函数
def score_display():
    l = response_score()
    if(l == 0):
        msg = "本周暂无积分~"
        return msg
    
    else:
        msg = [
              ['','周赛积分榜','']
              ]
        rank = 1
        for i in l:
            msg.append([rank,i['username'],i['score']])
            rank += 1
        
        row = len(msg)
        i = 0
        h_line = []
        while i < row:
            h_line.append(i)
            i += 1

        img = create_table(800, 80*row, _font_path, 30, row, 3, msg, h_line, [0,1,2])
        img.save('score.png')
        img = MessageSegment.image('file:///' + os.path.abspath('score.png'))

        return img

#沉淀值数据
def response_uestc():
    r = response(url_uestc)
    return r

#uestc的展示函数
def uestc_display():
    l = response_uestc()
    msg = [
          ['','沉淀值排行榜','']
          ]
    rank = 1
    for i in l:
        msg.append([rank,i['username'],i['score']])
        rank += 1
        if rank > 10:
            break
    
    row = len(msg)
    i = 0
    h_line = []
    while i < row:
        h_line.append(i)
        i += 1

    img = create_table(800, 80*row, _font_path, 30, row, 3, msg, h_line, [0,1,2])
    img.save('uestc.png')
    img = MessageSegment.image('file:///' + os.path.abspath('uestc.png'))

    return img
