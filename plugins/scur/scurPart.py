from nonebot.adapters.onebot.v11 import MessageSegment 
import os
import base64

from .data_source import _font_path, url_scuca
from .utils import create_table, time_convert, response

url_scur = f'{url_scuca}scur/'


def response_scur():
    """获取川大纪录，失败返回 0"""
    r = response(url_scur)
    return r if r else 0


def _align_records(avg, best):
    """
    对齐平均成绩和单次成绩的项目列表
    
    如果两个列表中的项目不一致，则补齐缺失项目
    """
    for i, j in zip(avg, best):
        if j['event'] != i['event']:
            avg.insert(avg.index(i), {
                'event': j['event'],
                'username': j['username'],
                'avg': 0
            })
    
    # 补齐长度差异
    while len(avg) < len(best):
        avg.append({
            'event': best[len(avg)]['event'],
            'username': best[len(avg)]['username'],
            'avg': 0
        })
    
    return avg, best


def record():
    """
    将川大纪录的文本内容存入二维列表
    
    Returns:
        list: 二维列表（表格数据）或字符串（无纪录提示）
    """
    r = response_scur()
    
    if r == 0 or not r.get('avg'):
        return "暂无纪录~"
    
    msg = [
        ['', '', 'SCU RECORD', '', ''],
        ['单', '次', '项目', '平', '均'],
    ]
    
    avg, best = _align_records(r['avg'], r['best'])
    
    # 构建表格数据行
    for avg_record, best_record in zip(avg, best):
        msg.append([
            time_convert(best_record['best']),
            best_record['username'],
            avg_record['event'],
            avg_record['username'],
            time_convert(avg_record['avg'])
        ])
    
    return msg


def record_display():
    """生成并返回川大纪录的表格图片"""
    text = record()
    
    if isinstance(text, str):
        return text
    
    row_count = len(text)
    h_lines = list(range(row_count + 1))  # 每一行都有横线
    v_lines = [2]  # 第三列竖线
    
    img = create_table(1200, 80 * row_count, _font_path, 30, row_count, 5, text, h_lines, v_lines)
    img.save('scur.png')
    
    with open('scur.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    img = MessageSegment.image('base64://' + encoded_image)
    os.remove('scur.png')
    
    return img


