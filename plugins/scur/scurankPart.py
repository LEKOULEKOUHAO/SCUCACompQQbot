from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import  _font_path, url_scuca
from .utils import response, time_convert, event_convert, create_table

#各项目top10, event:项目, aorb：avg or best, 每一页十条成绩, page=1即请求前十条成绩
def url_rank(event:str,aorb:str):
    url_rank = f'{url_scuca}rank/{event}/{aorb}/?page=1'
    return url_rank

#历史前十,event:项目,aorb: avg or best,若没有返回为0
def response_rank_result(event:str,aorb:str):
    r = response(url_rank(event,aorb))['results']
    if(r):
        return r
    else:
        return 0
    
#将scurank的文本内容存入二维列表msg
def top10(event:str):
    r_avg = response_rank_result(event,'avg')
    r_best = response_rank_result(event,'best')

    if(r_avg == 0):
        msg = "当前暂无该项目历史成绩记录~"
    else:
        msg = [
              ['',event_convert(event),'单次  ||  平均',''],
              ]

        for i,j in zip(r_avg,r_best):
            msg.append([time_convert(j['best']),j['username'],i['username'],time_convert(i['avg'])])

    return msg

#scurank的展示函数, event:项目
def top10_display(event:str):
    text = top10(event)
    if text == "当前暂无该项目历史成绩记录~":
        return text
    else:
        row = len(text)
        i = 0
        h_line = []
        v_line = []
        while i <= row:
            h_line.append(i) # 每一行都有横线 
            i += 1
        
        img = create_table(1200, 80*row, _font_path, 30, row, 4, text, h_line, v_line)
        img.save('top10.png')
        with open('top10.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        img = MessageSegment.image('base64://' + encoded_image)
        os.remove('top10.png')

        return img