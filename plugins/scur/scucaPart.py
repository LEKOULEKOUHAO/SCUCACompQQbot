from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .data_source import _font_path, url_scuca
from .utils import create_table, time_convert, response


def url_userdata(username: str) -> str:
    """生成查询某一选手官方成绩的URL"""
    return f'{url_scuca}user/data/{username}'


def response_userdata(username: str):
    """
    获取某用户的官方成绩数据
    
    Returns:
        dict: 用户数据
        -1: 用户不存在
        0: 用户已注册但还没有成绩记录
    """
    r = response(url_userdata(username))
    
    # 检查是否用户不存在
    if 'detail' in r:
        if r['detail'] == '用户不存在！':
            return -1
    
    # 检查是否有平均成绩
    if 'avg' in r:
        return r if r['avg'] else 0


def scuca_display(username: str):
    """
    显示某一选手的SCUCA官方成绩
    
    Args:
        username: 用户名
    
    Returns:
        str或MessageSegment: 成绩信息或错误提示
    """
    r = response_userdata(username)
    
    if r == -1:
        return "输入的选手名未注册或不存在,你是不是输错了捏😠"
    elif r == 0:
        return f"{username}暂无SCUCA官方成绩~"
    
    # 构建成绩表格
    msg = [
        ['', f'SCUCA官方成绩:    {username}     单次  ||  平均', '']
    ]
    
    for avg_record, best_record in zip(r['avg'], r['best']):
        msg.append([
            avg_record['event'],
            time_convert(best_record['best']),
            time_convert(avg_record['avg'])
        ])
    
    msg.append(['', f'沉淀值:  {r["score"]}', ''])
    
    # 生成表格图片
    row_count = len(msg)
    h_lines = list(range(row_count))
    
    img = create_table(800, 80 * row_count, _font_path, 30, row_count, 3, msg, h_lines, [])
    img.save('scuca.png')
    
    with open('scuca.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    img = MessageSegment.image('base64://' + encoded_image)
    os.remove('scuca.png')
    
    return img


