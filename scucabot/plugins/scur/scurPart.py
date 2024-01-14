from nonebot.adapters.onebot.v11 import MessageSegment 
import os

from .data_source import _font_path, url_scuca
from .utils import create_table, time_convert, response

url_scur = f'{url_scuca}scur/'#川大纪录

#川大纪录,若没有返回为0
def response_scur():
    r = response(url_scur)
    if(r):
        return r
    else:
        return 0

#将scur的文本内容存入二维列表msg
def record():
    r = response_scur()
    msg = ""
    if(r == 0):
        msg += "暂无纪录~"
    else:
        if not(r['avg']):
            msg += "暂无纪录~"
        else:
            msg = [
                  ['','','SCU RECORD','',''],
                  ['单','次','项目','平','均'],
                  ]
            avg = r['avg']
            best = r['best']

            for i,j in zip(avg,best):
                if(j['event'] != i['event']):
                    avg.insert(avg.index(i),{'event':j['event'],'username':j['username'],'avg':0})

            if len(avg) < len(best):#若avg和best长度不一致，将avg补齐，补齐成绩为DNF，选手为对应项目单次纪录拥有者
                avg.append({'event':best[-1]['event'],'username':best[-1]['username'],'avg':0})

            for i,j in zip(avg,best):
                msg.append([time_convert(j['best']),j['username'],i['event'],i['username'],time_convert(i['avg'])])

    return msg

def record_display():
    text= record()
    if text == "暂无纪录~":
        return text
    else:
        row = len(text)
        i = 0
        h_line = []
        v_line = [2]
        while i <= row:
            h_line.append(i) # 每一行都有横线 
            i += 1
        
        img = create_table(1200, 80*row, _font_path, 30, row, 5, text, h_line, v_line)
        img.save('scur.png')
        img = MessageSegment.image('file:///' + os.path.abspath('scur.png'))

        return img

