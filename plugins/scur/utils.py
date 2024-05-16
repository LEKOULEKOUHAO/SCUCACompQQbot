import re

import requests
import json
from PIL import Image, ImageDraw, ImageFont

#从接口请求数据,处理为json
def response(url:str):
    response = requests.get(url).text
    response_json = json.loads(response)
    return response_json

#时间转换函数，以 分：秒 形式展示，秒保留三位小数, 0代表DNF
def time_convert(time:float):
    if time == 0:
        return "DNF"
    else:
        m = int(time // 60) #分钟数，time除以60取整
        s = float(time % 60) #秒数，time除以60取余
        if m != 0:
            if s < 10:
                return '{}:0{:.3f}'.format(m,s)#如遇到67转换为1:07.000
            else:
                return '{}:{:.3f}'.format(m,s)
        if m == 0:
            return '{:.3f}'.format(s)

# 制表，width:图片宽度，height:图片高度，font_path:字体文件路径，font_size:字体大小，rows:行数，cols:列数，text:文本内容，
# h_lines:水平线列表，v_lines:竖线列表，align:单元格对齐方式，默认为居中对齐，可选参数有：'left'左对齐，'right'右对齐
def create_table(width, height, font_path, font_size, rows, cols, text, h_lines=None, v_lines=None, align='center'):
    # 创建空白图片
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建画笔
    draw = ImageDraw.Draw(image)
    # 加载字体
    font = ImageFont.truetype(font_path, font_size)
    # 计算单元格宽度和高度
    col_width = width // cols
    row_height = height // rows
    # 绘制单元格和文字
    for row in range(rows):
        for col in range(cols):
            cell_x = col * col_width
            cell_y = row * row_height
            # 绘制竖线
            if v_lines is None or col in v_lines:
                draw.rectangle((cell_x, cell_y, cell_x + col_width, cell_y + row_height), outline=(0, 0, 0))
            # 绘制文字
            if row < len(text) and col < len(text[row]):
                cell_text = text[row][col]
                text_width, text_height = font.getsize(str(cell_text))
                if align == 'center':
                    text_x = cell_x + (col_width - text_width) // 2
                elif align == 'right':
                    text_x = cell_x + col_width - text_width - 5
                else:
                    text_x = cell_x + 5
                text_y = cell_y + (row_height - text_height) // 2
                draw.text((text_x, text_y), str(cell_text), fill=(0, 0, 0), font=font)
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
    # 返回图片
    return image

#在scurank展示时用到,event:项目
def event_convert(event:str):
    match event:
        case "222":
            msg = "二阶速拧  SCU  历史TOP10"
        case "333":
            msg = "三阶速拧  SCU  历史TOP10"
        case "444":
            msg = "四阶速拧  SCU  历史TOP10"
        case "555":
            msg = "五阶速拧  SCU  历史TOP10"
        case "666":
            msg = "六阶速拧  SCU  历史TOP10"
        case "777":
            msg = "七阶速拧  SCU  历史TOP10"
        case "skewb":
            msg = "斜转魔方  SCU  历史TOP10"
        case "pyra":
            msg = "金字塔  SCU  历史TOP10"
        case "sq1":
            msg = "SQ1  SCU  历史TOP10"
        case "minx":
            msg = "五魔方  SCU  历史TOP10"
        case "clock":
            msg = "魔表  SCU  历史TOP10"
        case "333oh":
            msg = "三阶单手  SCU  历史TOP10"
        case "333bld":
            msg = "三阶盲拧  SCU  历史TOP10"
        case "444bld":
            msg = "四阶盲拧  SCU  历史TOP10"
        case "555bld":
            msg = "五阶盲拧  SCU  历史TOP10"
    return msg

#发打乱用，event:项目
def event_convert2(event:re.Match):
    cubeevent = event.string
    match event.string:
        case"/2":
            cubeevent = "222"
        case"/3":
            cubeevent = "333"
        case"/4":
            cubeevent = "444"
        case"/5":
            cubeevent = "555"
        case"/6":
            cubeevent = "666"
        case"/7":
            cubeevent = "777"
        case"/3oh":
            cubeevent = "333oh"
        case"/3bf":
            cubeevent = "333bld"
        case"/4bf":
            cubeevent = "444bld"
        case"/5bf":
            cubeevent = "555bld"
        case"/sq":
            cubeevent = "sq1"
        case"/py":
            cubeevent = "pyra"
        case"/sk":
            cubeevent = "skewb"
        case"/clock":
            cubeevent = "clock"
        case"/minx":
            cubeevent = "minx"

    return cubeevent
