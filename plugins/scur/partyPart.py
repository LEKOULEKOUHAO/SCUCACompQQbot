from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image, ImageDraw, ImageFont
import random
import os
import time
import base64

from .data_source import jiangan_food, wangjiang_food, _font_path, _font_path_xingkai, _font_path_hupo, reward_background


# 聚会地点映射
PARTY_LOCATIONS = {
    '江安': 0,
    '望江': 1,
}


def party_display():
    """随机选择聚会地点"""
    location = random.choice(list(PARTY_LOCATIONS.keys()))
    party_flag = PARTY_LOCATIONS[location]
    msg = f'去{location}聚！'
    return msg, party_flag


def eat_display(party_flag):
    """根据聚会地点选择餐厅"""
    food_options = jiangan_food if party_flag == 0 else wangjiang_food
    restaurant = random.choice(food_options)
    return f'吃{restaurant}!'


def _generate_pairings(username_list: list) -> str:
    """生成配对字符串，返回配对结果"""
    pairings = []
    while len(username_list) > 0:
        r1 = random.choice(username_list)
        username_list.remove(r1)
        r2 = random.choice(username_list)
        username_list.remove(r2)
        pairings.append(f'{r1} vs {r2}')
    return '\n'.join(pairings)


def draw_display(num=None, username_list=None):
    """
    抽签功能
    
    Args:
        num: 参赛人数
        username_list: 参赛选手名单
    """
    if username_list is None:
        username_list = list(range(1, num + 1))
    
    if len(username_list) < 3:
        return '人数过少，无法抽签！'
    
    # 奇数人数处理
    if len(username_list) % 2 == 1:
        bye_player = random.choice(username_list)
        username_list.remove(bye_player)
        
        # 随机决定是轮空还是淘汰
        result_type = random.choice(['轮空了', '淘汰了'])
        msg = f'{bye_player}{result_type}！\n正常抽签:\n'
        msg += _generate_pairings(username_list)
        return msg
    
    # 偶数人数正常抽签
    msg = '正常抽签:\n'
    msg += _generate_pairings(username_list)
    return msg


def _create_reward_image(
    rank: str,
    rank_text: str,
    username: str,
    cubeevent: str,
    img_size: tuple,
    background_image: Image.Image,
    font_title: ImageFont.FreeTypeFont,
    font_rank: ImageFont.FreeTypeFont,
    font: ImageFont.FreeTypeFont,
    font_date: ImageFont.FreeTypeFont
) -> MessageSegment:
    """
    创建单个奖励图片
    
    Args:
        rank: 排名（冠军、亚军、季军）
        rank_text: 排名显示文本
        username: 获奖人名字
        cubeevent: 魔方项目
        img_size: 图片大小
        background_image: 背景图片
        font_title: 标题字体
        font_rank: 排名字体
        font: 普通字体
        font_date: 日期字体
    
    Returns:
        MessageSegment 对象
    """
    img = Image.new('RGBA', img_size)
    img.paste(background_image, (0, 0))
    
    draw = ImageDraw.Draw(img)
    draw.text((img_size[0] / 2 - 75, 70), '战神杯', fill='black', font=font_title)
    draw.text((img_size[0] / 2 - 100, 230), rank_text, fill='red', font=font_rank)
    draw.text((img_size[0] / 2 - 175, 350), f'获奖人：{username}', fill='black', font=font)
    draw.text((img_size[0] / 2 - 125, 420), f'项目：{cubeevent}', fill='black', font=font)
    
    # 右下角添加日期
    current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    draw.text((img_size[0] - 180, img_size[1] - 30), current_date, fill='black', font=font_date)
    
    # 保存为临时文件
    temp_filename = f'reward_{rank}.png'
    img.save(temp_filename)
    
    with open(temp_filename, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    result = MessageSegment.image('base64://' + encoded_image)
    os.remove(temp_filename)
    
    return result


def reward_display(cubeevent, username1, username2, username3):
    """发奖功能，生成三张奖励图片"""
    img_size = (800, 600)
    
    # 加载背景图片
    background = Image.open(reward_background).resize(img_size)
    
    # 加载字体
    font_title = ImageFont.truetype(_font_path_hupo, 50)
    font_rank = ImageFont.truetype(_font_path_xingkai, 100)
    font = ImageFont.truetype(_font_path, 50)
    font_date = ImageFont.truetype(_font_path, 30)
    
    # 生成三个奖励图片
    img1 = _create_reward_image('冠军', '冠军', username1, cubeevent, img_size, background, font_title, font_rank, font, font_date)
    img2 = _create_reward_image('亚军', '亚军', username2, cubeevent, img_size, background, font_title, font_rank, font, font_date)
    img3 = _create_reward_image('季军', '季军', username3, cubeevent, img_size, background, font_title, font_rank, font, font_date)
    
    return img1, img2, img3
