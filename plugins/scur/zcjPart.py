from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import CubeEvent, _font_path
from .utils import create_table, time_convert
from .weekrank_and_comprank_Part import response_week_ongoing
from .scorePart import url_score, response_score

#username:用户名, 返回-1代表用户未注册或本周暂无成绩，否则返回该用户本周成绩列表
def week_results(username:str):
    r = response_week_ongoing()['result_set']
    r = list(filter(lambda x:x['user'] == username,r))
    l = []
    if(r):

        for i in r:
            l.append({'event':i['event'],'avg':i['avg'],'best':i['best']})
            l.sort(key=lambda x:CubeEvent.index(x['event']))

        return l
    else:
        return -1

#weekresults的展示函数, username:用户名
def week_results_display(username:str):
    l = week_results(username)
    if(l == -1):
        msg = f"该用户未注册或本周暂无成绩~"
        return msg
    else:
        msg = [
              ['',f'周成绩:   {username}    单次  ||  平均','']
              ]
        for i in l:
            msg.append([i['event'],time_convert(i['best']),time_convert(i['avg'])])

        data_score = response_score()
        for user in data_score:
            if(user['username'] == username):
                msg.append(['','周赛积分:  '+str(user['score']),''])
                break

        row = len(msg)
        i = 0
        h_line = []
        while i < row:
            h_line.append(i)
            i += 1

        img = create_table(800, 80*row, _font_path, 30, row, 3, msg, h_line, [])
        img.save('weekresults.png')
        with open('weekresults.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        img = MessageSegment.image('base64://' + encoded_image)
        os.remove('weekresults.png')

        return img