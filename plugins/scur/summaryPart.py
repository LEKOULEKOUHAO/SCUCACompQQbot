from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import _font_path, CubeEvent
from .weekrank_and_comprank_Part import response_week_ongoing, week_list
from .utils import create_table, time_convert


# 需要特殊处理的事件（3轮制而非5轮制）
THREE_ATTEMPT_EVENTS = {'666', '777', '333bld', '444bld', '555bld'}


def _build_event_result_row(participant: dict, event: str) -> list:
    """
    构建单个参赛者的成绩行
    
    Args:
        participant: 参赛者数据
        event: 项目代码
    
    Returns:
        list: 表格行数据
    """
    base_row = [
        participant['user'],
        time_convert(participant['avg']),
        time_convert(participant['best']),
    ]
    
    if event in THREE_ATTEMPT_EVENTS:
        # 3轮制
        return base_row + [time_convert(participant['time_1']), '', time_convert(participant['time_2'])]
    else:
        # 5轮制
        return base_row + [
            time_convert(participant['time_1']),
            time_convert(participant['time_2']),
            time_convert(participant['time_3']),
            time_convert(participant['time_4']),
            time_convert(participant['time_5'])
        ]


def summary_display_event(event: str):
    """
    显示某一项目的本周成绩总结
    
    Args:
        event: 项目代码
    
    Returns:
        MessageSegment: 成绩表格图片或 -1 (无人参赛)
    """
    l = week_list(event)
    if not l:
        return -1  # 此项目无人参赛
    
    msg = [
        [f'{event}  Top3', '平均', '单次', '详细成绩', '', f'(该项目共{len(l)}人参赛)']
    ]
    
    # 取前3名
    for participant in l[:3]:
        msg.append(_build_event_result_row(participant, event))
    
    # 生成表格
    row_count = len(msg)
    h_lines = list(range(row_count + 1))
    v_lines = [0, 1, 2]
    
    img = create_table(1500, 80 * row_count, _font_path, 30, row_count, 8, msg, h_lines, v_lines)
    temp_filename = f'summary_{event}.png'
    img.save(temp_filename)
    
    with open(temp_filename, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    result = MessageSegment.image('base64://' + encoded_image)
    os.remove(temp_filename)
    
    return result


def summary_display():
    """生成周赛总结"""
    r = response_week_ongoing()
    msg = []
    
    if r:
        msg.append("上周周赛已完结！各项目前三如下~")
        for event in CubeEvent:
            event_summary = summary_display_event(event)
            if event_summary != -1:
                msg.append(event_summary)
        msg.append("本周周赛已开启~")
    else:
        msg = "暂无正在进行的周赛"
    
    return msg
