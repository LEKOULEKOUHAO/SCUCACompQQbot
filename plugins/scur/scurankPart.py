from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import _font_path, url_scuca
from .utils import response, time_convert, event_convert, create_table


def url_rank(event: str, aorb: str) -> str:
    """
    生成排名查询URL
    
    Args:
        event: 项目代码
        aorb: 'avg' 或 'best'
    
    Returns:
        str: 完整的API URL
    """
    return f'{url_scuca}rank/{event}/{aorb}/?page=1'


def response_rank_result(event: str, aorb: str):
    """
    获取某项目的历史排名成绩
    
    Args:
        event: 项目代码
        aorb: 'avg' 或 'best'
    
    Returns:
        list: 成绩列表，若无结果返回 0
    """
    results = response(url_rank(event, aorb))['results']
    return results if results else 0


def top10(event: str):
    """
    生成某项目的Top10成绩表格数据
    
    Args:
        event: 项目代码
    
    Returns:
        list: 二维表格数据或错误提示字符串
    """
    r_avg = response_rank_result(event, 'avg')
    r_best = response_rank_result(event, 'best')
    
    if r_avg == 0:
        return "当前暂无该项目历史成绩记录~"
    
    msg = [
        ['', event_convert(event), '单次  ||  平均', ''],
    ]
    
    for avg_record, best_record in zip(r_avg, r_best):
        msg.append([
            time_convert(best_record['best']),
            best_record['username'],
            avg_record['username'],
            time_convert(avg_record['avg'])
        ])
    
    return msg


def top10_display(event: str):
    """
    显示某项目的Top10成绩表格
    
    Args:
        event: 项目代码
    
    Returns:
        str或MessageSegment: 表格图片或错误提示
    """
    text = top10(event)
    
    if isinstance(text, str):
        return text
    
    row_count = len(text)
    h_lines = list(range(row_count + 1))
    v_lines = []
    
    img = create_table(1200, 80 * row_count, _font_path, 30, row_count, 4, text, h_lines, v_lines)
    img.save('top10.png')
    
    with open('top10.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    img = MessageSegment.image('base64://' + encoded_image)
    os.remove('top10.png')
    
    return img
