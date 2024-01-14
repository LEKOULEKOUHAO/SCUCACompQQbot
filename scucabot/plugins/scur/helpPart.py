from nonebot.adapters.onebot.v11 import MessageSegment
import os

from .data_source import _font_path, url_scuca
from .utils import create_table

def web_display():
    return 'https://scu.yougi.top/'

def help_display():
    text = [
               ['Command', '功能', '中文命令'],
               ['/about','关于','/关于'],
               ['','赛事部分',''],
               ['/scur', '查看各项目的协会纪录', '/纪录'],
               ['/scuca [选手名]', '开某一选手的SCUCA官方成绩', '/开盒 | /开 | /盒 [选手名]'],
               ['/scurank [项目]', '查看某一项目的协会历史前十', '/总排名 [项目]'],
               ['/weekrank [项目]', '查看某一项目的当前周赛排名', '/周排名 [项目]'],
               ['/comprank  [项目]', '查看某一项目的当前正赛排名', '/比赛排名 [项目]'],
               ['/pk [选手1] [选手2]', '比较两个选手的成绩', '/打架 [选手1] [选手2]'],
               ['/zcj [选手名]', '查看某一选手的本周成绩', '/周成绩 [选手名]'],
               ['/score', '查看本周积分榜', '/积分榜'],
               ['/uestc', '查看沉淀值(总积分)榜(取前十)', '/沉淀值'],
               ['/web' , '查看社团网站' , '/网站'],
               ['','聚会部分',''],
                ['/party', '随机选择江安或望江', '/聚会'],
                ['/eat', '随机选择去(聚会所在地)哪吃', '/吃'],
                ['/draw [人数]', '抽签(也支持直接输入选手名)', '/抽签 [人数]'],
                ['/reward [项目] [冠] [亚] [季]','战神杯获奖证书','/发奖 [项目] [冠] [亚] [季]'],
                 ['','面向群u需求部分',''],
                 ['/travel ([地名])','让bot帮你决定去哪旅游(提出者:铁铂)','/润 ([地名])'],
                 ['/wca  [WCA ID]','查询WCA官方成绩(提出者:李温柔)','/官方 [WCA ID]'],
            
            ['','pk各项目命令:/2|/3|/4|/5|/6|/7|/sq|/sk|/minx|/py|/3oh|/3bf|/4bf|/5bf|/clock',''],
            ['','(ps:如遇bug联系QQ:3226855380修复)','']
                
            ]
    i = 0
    h_line = []
    while i <= len(text):
        h_line.append(i) # 每一行都有横线 
        i += 1
    img = create_table(1200, 1560, _font_path, 30, len(text), 3, text, h_line, [])
    img.save('help.png')
    img = MessageSegment.image('file:///' + os.path.abspath('help.png'))

    return img
