from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .utils import create_table, response
from .data_source import _font_path, url_scuca

url_score = f'{url_scuca}competition/week/score/'  # 积分榜
url_uestc = f'{url_scuca}rank/score/'  # 沉淀值榜


def response_score():
    """获取本周积分数据，无数据返回0"""
    r = response(url_score)
    return r if r else 0


def response_uestc():
    """获取沉淀值排行数据"""
    return response(url_uestc)


def _create_ranking_image(data: list, title: str, filename: str, max_rows: int = None) -> MessageSegment:
    """
    创建排行榜图片
    
    Args:
        data: 排行数据列表
        title: 排行榜标题
        filename: 临时保存的文件名
        max_rows: 最多显示的行数（不包括标题）
    
    Returns:
        MessageSegment 图片对象
    """
    if max_rows:
        data = data[:max_rows]
    
    msg = [['', title, '']]
    
    for rank, record in enumerate(data, 1):
        msg.append([rank, record['username'], record['score']])
    
    row_count = len(msg)
    h_lines = list(range(row_count))
    v_lines = [0, 1, 2]
    
    img = create_table(800, 80 * row_count, _font_path, 30, row_count, 3, msg, h_lines, v_lines)
    img.save(filename)
    
    with open(filename, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    result = MessageSegment.image('base64://' + encoded_image)
    os.remove(filename)
    
    return result


def score_display():
    """积分榜的展示函数"""
    l = response_score()
    if l == 0:
        return "本周暂无积分~"
    
    return _create_ranking_image(l, '周赛积分榜', 'score.png')


def uestc_display():
    """沉淀值排行榜的展示函数"""
    l = response_uestc()
    return _create_ranking_image(l, '沉淀值排行榜', 'uestc.png', max_rows=10)

