from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import _font_path, url_scuca
from .utils import create_table, time_convert, response

url_competition_week_ongoing = f'{url_scuca}competition/week/ongoing/' #正在进行的周赛
url_competition_special_ongoing = f'{url_scuca}competition/special/ongoing/' #正在进行的正赛

#周赛数据，若没有正在进行的周赛返回0
def response_week_ongoing():
    r = response(url_competition_week_ongoing)
    if('ongoing' in r):
        return r
    else:
        return 0

#正赛数据,若没有正在进行的正赛返回0
def response_special_ongoing():
    r = response(url_competition_special_ongoing)
    if('ongoing' in r):
        return r
    else:
        return 0

#用于提取周赛某一项目的所有已上传成绩并以avg排序，event：项目名(排序时将0即DNF处理为无穷)
def week_list(event:str):
    l = response_week_ongoing()['result_set']
    list_week = list(filter(lambda x:x['event'] == event,l))
    #盲拧按单次成绩排序
    if event in ['333bld','444bld','555bld']:
        list_week.sort(key = lambda x:x['best'] if x['best'] > 0 else float("inf"))
    else:
        list_week.sort(key = lambda x:x['avg'] if x['avg'] > 0 else float("inf"))

    return list_week

#用于提取正赛某一项目的所有已上传成绩并以avg排序，event：项目名(排序时将0即DNF处理为无穷)
def spec_list(event:str):
    l = response_special_ongoing()['result_set']
    list_spec = list(filter(lambda x:x['event'] == event,l))
    #盲拧按单次成绩排序
    if event in ['333bld','444bld','555bld']:
        list_spec.sort(key = lambda x:x['best'] if x['best'] > 0 else float("inf"))
    else:
        list_spec.sort(key = lambda x:x['avg'] if x['avg'] > 0 else float("inf"))
        
    return list_spec

#用于获取比赛开设项目数，参赛人数
def week_comp_info(dic:dict):
    if(dic):
        user_count = dic['user_count']
        event_count = dic['event_count']
        msg = f"共开设{event_count}个项目,已有{user_count}人参赛)"
    else:
        msg = ""
    
    return msg

def spec_comp_info(dic:dict):
    if(dic):
        user_count = dic['user_count']
        event_count = dic['event_count']
        msg = f"开设{event_count}个项目,共有{user_count}人报名)"
    else:
        msg = ""
    
    return msg

#周赛信息展示
def week_info_display():
    r = response_week_ongoing()
    msg = "(本周"
    msg += week_comp_info(r)
    return msg

#正赛信息展示
def comp_info_display():
    r = response_special_ongoing()
    msg = f"({r['compId']}"
    msg += spec_comp_info(r)
    return msg

#weekrank的展示函数, event:项目
def week_display(event:str):
    l = week_list(event)
    if (l):
        msg = [
              [f'RANK {event}','平均','单次','详细成绩','',week_info_display()]
              ]
        if event in ['666','777','333bld','444bld','555bld']:
            for i in l:
                msg.append([i['user'],time_convert(i['avg']),time_convert(i['best']),time_convert(i['time_1']),'',time_convert(i['time_2']),'',time_convert(i['time_3'])])
        else:
            for i in l:
                msg.append([i['user'],time_convert(i['avg']),time_convert(i['best']),time_convert(i['time_1']),time_convert(i['time_2']),time_convert(i['time_3']),time_convert(i['time_4']),time_convert(i['time_5'])])
        
        row = len(msg)
        i = 0
        h_line = []
        while i <= row:
            h_line.append(i) # 每一行都有横线 
            i += 1

        v_line = [0,1,2]

        img = create_table(1500, 80*row, _font_path, 30, row, 8, msg, h_line, v_line)
        img.save('weekrank.png')
        with open('weekrank.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        img = MessageSegment.image('base64://' + encoded_image)
        os.remove('weekrank.png')

        return img
    
    else:
        msg = "本周周赛暂无该项目成绩记录~"
        return msg

#comprank的展示函数, event:项目
def spec_display(event:str):
    l = spec_list(event)
    if (l):
        msg = [
              [f'RANK {event}','平均','单次','详细成绩','',comp_info_display()]
              ]
        if event in ['666','777','333bld','444bld','555bld']:
            for i in l:
                msg.append([i['user'],time_convert(i['avg']),time_convert(i['best']),time_convert(i['time_1']),'',time_convert(i['time_2']),'',time_convert(i['time_3'])])
        else:
            for i in l:
                msg.append([i['user'],time_convert(i['avg']),time_convert(i['best']),time_convert(i['time_1']),time_convert(i['time_2']),time_convert(i['time_3']),time_convert(i['time_4']),time_convert(i['time_5'])])
        
        row = len(msg)
        i = 0
        h_line = []
        while i <= row:
            h_line.append(i) # 每一行都有横线 
            i += 1

        v_line = [0,1,2]

        img = create_table(1500, 80*row, _font_path, 30, row, 8, msg, h_line, v_line)
        img.save('comprank.png')
        with open('comprank.png', 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        img = MessageSegment.image('base64://' + encoded_image)

        return img
           
    else:
        msg += "本次比赛暂无该项目成绩记录~"

    return msg