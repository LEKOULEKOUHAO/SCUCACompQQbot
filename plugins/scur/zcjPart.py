from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import CubeEvent, _font_path
from .utils import create_table, time_convert
from .weekrank_and_comprank_Part import response_week_ongoing
from .scorePart import response_score


def week_results(username: str):
    """
    获取某用户本周的成绩列表
    
    Args:
        username: 用户名
    
    Returns:
        list: 成绩列表
        -1: 用户未注册或本周暂无成绩
    """
    weekly_data = response_week_ongoing()
    if not weekly_data:
        return -1
    
    result_set = weekly_data.get('result_set', [])
    user_results = [r for r in result_set if r['user'] == username]
    
    if not user_results:
        return -1
    
    # 构建成绩列表并按项目顺序排序
    scores = [
        {
            'event': r['event'],
            'avg': r['avg'],
            'best': r['best']
        }
        for r in user_results
    ]
    scores.sort(key=lambda x: CubeEvent.index(x['event']))
    
    return scores


def week_results_display(username: str):
    """
    显示某用户本周的成绩表格
    
    Args:
        username: 用户名
    
    Returns:
        str或MessageSegment: 成绩表格图片或错误提示
    """
    scores = week_results(username)
    
    if scores == -1:
        return "该用户未注册或本周暂无成绩~"
    
    msg = [
        ['', f'周成绩:   {username}    单次  ||  平均', '']
    ]
    
    for score in scores:
        msg.append([
            score['event'],
            time_convert(score['best']),
            time_convert(score['avg'])
        ])
    
    # 添加周赛积分
    score_data = response_score()
    if score_data != 0:
        for user in score_data:
            if user['username'] == username:
                msg.append(['', f'周赛积分:  {user["score"]}', ''])
                break
    
    # 生成表格
    row_count = len(msg)
    h_lines = list(range(row_count))
    
    img = create_table(800, 80 * row_count, _font_path, 30, row_count, 3, msg, h_lines, [])
    img.save('weekresults.png')
    
    with open('weekresults.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    img = MessageSegment.image('base64://' + encoded_image)
    os.remove('weekresults.png')
    
    return img
