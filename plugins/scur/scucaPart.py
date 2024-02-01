from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import _font_path, url_scuca
from .utils import create_table, time_convert, response

#某一选手的官方成绩, username:选手名
def url_userdata(username:str):
    url_userdata = f'{url_scuca}user/data/{username}'
    return url_userdata

#某用户的官方成绩数据,username:用户名,若用户不存在返回-1,若用户已注册但还没有成绩记录返回0
def response_userdata(username:str):
    r = response(url_userdata(username))
    if('detail' in r):
        if(r['detail'] == '用户不存在！'):
            return -1 #用户不存在
    elif('avg' in r):
        if(r['avg']):
            return r
        else:
            return 0 #用户注册了但avg为空，说明还没有成绩记录
        
#scuca的展示函数, username:用户名
def scuca_display(username:str):
    r = response_userdata(username)
    if (r == -1):
        msg = "输入的选手名未注册或不存在,你是不是输错了捏😠"
        return msg
    elif (r == 0):
        msg = f"{username}暂无SCUCA官方成绩~"
        return msg
    else:
        msg = [
                ['',f'SCUCA官方成绩:    {username}     单次  ||  平均','']
              ]
        
        for i,j in zip(r['avg'],r['best']):
            msg.append([i['event'],time_convert(j['best']),time_convert(i['avg'])])

        msg.append(['','沉淀值:  '+str(r['score']),''])
        
        row = len(msg)
        i = 0
        h_line = []
        while i < row:
            h_line.append(i) # 每一行都有横线 
            i += 1

        img = create_table(800, 80*row, _font_path, 30, row, 3, msg, h_line, [])
        img.save('scuca.png')
        with open('scuca.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        img = MessageSegment.image('base64://' + encoded_image)
        os.remove('scuca.png')

        return img

