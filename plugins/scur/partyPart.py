from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image, ImageDraw, ImageFont
import random
import os
import time
import base64

from .data_source import jiangan_food, wangjiang_food,  _font_path, _font_path_xingkai, _font_path_hupo,reward_background

def party_display():
    r = random.choice(['江安','望江'])
    if r == '江安':
        party_flag = 0
    else:
        party_flag = 1

    msg = f'去{r}聚！'
    return msg, party_flag

def eat_display(party_flag):
    if party_flag == 0:
        r = random.choice(jiangan_food)
    else:
        r = random.choice(wangjiang_food)
    msg = f'吃{r}!'
    return msg

def draw_display(num = None, username_list = None):
    if username_list == None:
        username_list = []
        i = 1
        while i <= num:
            username_list.append(i)
            i += 1

    if len(username_list) < 3:
        msg = '人数过少，无法抽签！'
        return msg
    else:
        if len(username_list) % 2 == 1:
            r = random.choice(username_list)
            username_list.remove(r)
            if random.random() < 0.5:
                msg = f'{r}轮空了！'
                while len(username_list) > 0:
                    r1 = random.choice(username_list)
                    username_list.remove(r1)
                    r2 = random.choice(username_list)
                    username_list.remove(r2)
                    msg += f'\n{r1} vs {r2}'
                return msg
            else:
                msg = f'{r}淘汰了！'
                while len(username_list) > 0:
                    r1 = random.choice(username_list)
                    username_list.remove(r1)
                    r2 = random.choice(username_list)
                    username_list.remove(r2)
                    msg += f'\n{r1} vs {r2}'
                return msg
        else:
            msg = '正常抽签:'
            while len(username_list) > 0:
                r1 = random.choice(username_list)
                username_list.remove(r1)
                r2 = random.choice(username_list)
                username_list.remove(r2)
                msg += f'\n{r1} vs {r2}'
            return msg

def reward_display(cubeevent, username1, username2, username3):
    img_size = (800, 600)
    
    # Load the background image
    background = Image.open(reward_background).resize(img_size)
    
    img1 = Image.new('RGBA', img_size)
    img1.paste(background, (0, 0))
    
    font_title = ImageFont.truetype(_font_path_hupo, 50)
    font_rank = ImageFont.truetype(_font_path_xingkai, 100)
    font = ImageFont.truetype(_font_path, 50)
    font_date = ImageFont.truetype(_font_path, 30)
    draw = ImageDraw.Draw(img1)
    draw.text((img_size[0] / 2 - 75, 70), '战神杯', fill='black', font=font_title)
    draw.text((img_size[0] / 2 - 100, 230), f'冠军', fill='red', font=font_rank)
    draw.text((img_size[0] / 2 - 175, 350), '获奖人：' + username1, fill='black', font=font)
    draw.text((img_size[0] / 2 - 125, 420), '项目：'+ cubeevent, fill='black', font=font)
    #右下角添加日期
    draw.text((img_size[0] - 180, img_size[1] - 30), time.strftime('%Y-%m-%d', time.localtime(time.time())), fill='black', font=font_date)
    img1.save('reward1.png')
    with open('reward1.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    img1 = MessageSegment.image('base64://' + encoded_image)

    
    img2 = Image.new('RGBA', img_size)
    img2.paste(background, (0, 0))
    draw = ImageDraw.Draw(img2)
    draw.text((img_size[0] / 2 - 75, 70), '战神杯', fill='black', font=font_title)
    draw.text((img_size[0] / 2 - 100, 230), f'亚军', fill='red', font=font_rank)
    draw.text((img_size[0] / 2 - 175, 350), '获奖人：' + username2, fill='black', font=font)
    draw.text((img_size[0] / 2 - 125, 420), '项目：'+ cubeevent, fill='black', font=font)
    draw.text((img_size[0] - 180, img_size[1] - 30), time.strftime('%Y-%m-%d', time.localtime(time.time())), fill='black', font=font_date)
    img2.save('reward2.png')
    with open('reward2.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    img2 = MessageSegment.image('base64://' + encoded_image)
    
    img3 = Image.new('RGBA', img_size)
    img3.paste(background, (0, 0))
    draw = ImageDraw.Draw(img3)
    draw.text((img_size[0] / 2 - 75, 70), '战神杯', fill='black', font=font_title)
    draw.text((img_size[0] / 2 - 100, 230), f'季军', fill='red', font=font_rank)
    draw.text((img_size[0] / 2 - 175, 350), '获奖人：' + username3, fill='black', font=font)
    draw.text((img_size[0] / 2 - 125, 420), '项目：'+ cubeevent, fill='black', font=font)
    draw.text((img_size[0] - 180, img_size[1] - 30), time.strftime('%Y-%m-%d', time.localtime(time.time())), fill='black', font=font_date)
    img3.save('reward3.png')
    with open('reward3.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    img3 = MessageSegment.image('base64://' + encoded_image)
    
    
    os.remove('reward1.png')
    os.remove('reward2.png')
    os.remove('reward3.png')
    return img1, img2, img3