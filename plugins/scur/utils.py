import re
import requests
import json
from PIL import Image, ImageDraw, ImageFont


def response(url: str) -> dict:
    """从接口请求数据，处理为JSON格式"""
    response_text = requests.get(url).text
    return json.loads(response_text)


def time_convert(time: float) -> str:
    """
    时间转换函数，以 分：秒 形式展示，秒保留三位小数。
    0代表DNF（未完成）
    """
    if time == 0:
        return "DNF"
    
    minutes = int(time // 60)
    seconds = float(time % 60)
    
    if minutes > 0:
        return f'{minutes}:0{seconds:.3f}' if seconds < 10 else f'{minutes}:{seconds:.3f}'
    
    return f'{seconds:.3f}'



def create_table(
    width: int, 
    height: int, 
    font_path: str, 
    font_size: int, 
    rows: int, 
    cols: int, 
    text: list, 
    h_lines: list = None, 
    v_lines: list = None, 
    align: str = 'center'
) -> Image.Image:
    """
    创建文本表格图片
    
    Args:
        width: 图片宽度
        height: 图片高度
        font_path: 字体文件路径
        font_size: 字体大小
        rows: 行数
        cols: 列数
        text: 二维文本内容列表
        h_lines: 水平线所在行索引列表
        v_lines: 竖线所在列索引列表
        align: 单元格对齐方式，可选 'center'、'left'、'right'
    
    Returns:
        生成的图片对象
    """
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    
    col_width = width // cols
    row_height = height // rows
    
    # 绘制单元格和文字
    for row in range(rows):
        for col in range(cols):
            cell_x = col * col_width
            cell_y = row * row_height
            
            # 绘制单元格边框
            if v_lines is None or col in v_lines:
                draw.rectangle(
                    (cell_x, cell_y, cell_x + col_width, cell_y + row_height), 
                    outline=(0, 0, 0)
                )
            
            # 绘制单元格内文字
            if row < len(text) and col < len(text[row]):
                cell_text = str(text[row][col])
                text_bbox = font.getbbox(cell_text)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # 计算文本位置根据对齐方式
                if align == 'center':
                    text_x = cell_x + (col_width - text_width) // 2
                elif align == 'right':
                    text_x = cell_x + col_width - text_width - 5
                else:
                    text_x = cell_x + 5
                
                text_y = cell_y + (row_height - text_height) // 2
                draw.text((text_x, text_y), cell_text, fill=(0, 0, 0), font=font)
    
    # 绘制水平线
    if h_lines is not None:
        for row in h_lines:
            y = (row + 1) * row_height - 1
            draw.line((0, y, width, y), fill=(0, 0, 0))
    
    # 绘制竖线
    if v_lines is not None:
        for col in v_lines:
            x = (col + 1) * col_width - 1
            draw.line((x, 0, x, height), fill=(0, 0, 0))
    
    return image


# 事件显示文本映射字典
EVENT_DISPLAY_TEXT = {
    "222": "二阶速拧  SCU  现役TOP10",
    "333": "三阶速拧  SCU  现役TOP10",
    "444": "四阶速拧  SCU  现役TOP10",
    "555": "五阶速拧  SCU  现役TOP10",
    "666": "六阶速拧  SCU  现役TOP10",
    "777": "七阶速拧  SCU  现役TOP10",
    "skewb": "斜转魔方  SCU  现役TOP10",
    "pyra": "金字塔  SCU  现役TOP10",
    "sq1": "SQ1  SCU  现役TOP10",
    "minx": "五魔方  SCU  现役TOP10",
    "clock": "魔表  SCU  现役TOP10",
    "333oh": "三阶单手  SCU  现役TOP10",
    "333bld": "三阶盲拧  SCU  现役TOP10",
    "444bld": "四阶盲拧  SCU  现役TOP10",
    "555bld": "五阶盲拧  SCU  现役TOP10",
}

# 命令快捷键映射
COMMAND_EVENT_MAPPING = {
    "/2": "222",
    "/3": "333",
    "/4": "444",
    "/5": "555",
    "/6": "666",
    "/7": "777",
    "/3oh": "333oh",
    "/3bf": "333bld",
    "/4bf": "444bld",
    "/5bf": "555bld",
    "/sq": "sq1",
    "/py": "pyra",
    "/sk": "skewb",
    "/clock": "clock",
    "/minx": "minx",
}


def event_convert(event: str) -> str:
    """在scurank展示时使用，将事件代码转换为显示文本"""
    return EVENT_DISPLAY_TEXT.get(event, "未知项目")


def event_convert2(event: re.Match) -> str:
    """将命令快捷键转换为事件代码（用于打乱生成）"""
    return COMMAND_EVENT_MAPPING.get(event.string, event.string)

