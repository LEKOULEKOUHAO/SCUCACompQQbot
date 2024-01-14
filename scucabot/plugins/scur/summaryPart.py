from nonebot.adapters.onebot.v11 import MessageSegment
import os

from .data_source import _font_path, CubeEvent
from .weekrank_and_comprank_Part import response_week_ongoing, week_list
from .utils import create_table, time_convert

def summary_display():
    r = response_week_ongoing()
    if(r):
        msg = "本周周赛已完结！各项目前三如下~\n"
        for event in CubeEvent:
            if summary_display_event(event) != -1:
                msg += summary_display_event(event)
    else:
        msg = "暂无正在进行的周赛"
    
    return msg

def summary_display_event(event:str):
    l = week_list(event)
    if(l):
        msg = [
              [f'{event}  Top3','平均','单次','详细成绩','',f'(该项目共{len(l)}人参赛)']
              ]
        if event in ['666','777','333bld','444bld','555bld']:
            count = 0
            for i in l:
                count += 1
                msg.append([i['user'],time_convert(i['avg']),time_convert(i['best']),time_convert(i['time_1']),'',time_convert(i['time_2']),'',time_convert(i['time_3'])])
                if count == 3:
                    break
        else:
            count = 0
            for i in l:
                count += 1
                msg.append([i['user'],time_convert(i['avg']),time_convert(i['best']),time_convert(i['time_1']),time_convert(i['time_2']),time_convert(i['time_3']),time_convert(i['time_4']),time_convert(i['time_5'])])
                if count == 3:
                    break

        row = len(msg)
        i = 0
        h_line = []
        while i <= row:
            h_line.append(i) # 每一行都有横线 
            i += 1

        v_line = [0,1,2]

        img = create_table(1500, 80*row, _font_path, 30, row, 8, msg, h_line, v_line)
        img.save(f'summary_{event}.png')
        img = MessageSegment.image('file:///' + os.path.abspath(f'summary_{event}.png'))

        return img

    else:
        return -1 #此项目无人参赛