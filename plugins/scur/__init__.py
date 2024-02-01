from nonebot import on_command, on_notice, on_regex, get_bot, require
from nonebot.typing import T_State
from nonebot.params import CommandArg, RegexMatched
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, GroupIncreaseNoticeEvent, Bot, GROUP, Message
from nonebot.permission import SUPERUSER
#from nonebot_plugin_apscheduler import scheduler

from .helpPart import help_display, web_display
from .scurPart import record_display
from .scurankPart import top10_display
from .weekrank_and_comprank_Part import response_week_ongoing, response_special_ongoing, week_display, spec_display
from .scucaPart import scuca_display
from .pkPart import pk_display
from .scorePart import score_display, uestc_display
from .zcjPart import week_results_display
from .partyPart import eat_display, party_display, draw_display, reward_display
from .travelPart import travel_display
from .summaryPart import summary_display
from .scramblePart import scramble_display
from .wcaPart import wca_display
from .data_source import event_tips, CubeEvent, provincess, superusers
from .utils import response, event_convert2

#---------------------------------------------------------------------------------------------#
welcome = on_notice()
web = on_command("web", aliases={"网站"}, permission= GROUP, priority=1)
help = on_command("help", aliases={"帮助"}, permission= GROUP, priority=1)
about = on_command("about", aliases={"关于"}, permission= GROUP, priority=1)

@welcome.handle()
async def welcome(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user = event.get_user_id()
    at_ = "欢迎[CQ:at,qq={}]".format(user)
    msg = at_ + '加入🥳\n'
    msg += "社团网站为: https://scu.yougi.top/,若要在社团网站注册账号,请实名注册,注册后请在群里告知网站管理员后台审核通过🥰"
    msg = Message(msg)
    msg += SCUCABot.help(event)
    await bot.send(event,msg)

@help.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.help(event)
    await help.finish(msg)

@web.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.web(event)
    await web.finish(msg)

@about.handle()
async def _(event: GroupMessageEvent):
    msg = "本项目为四川大学魔方协会SCUCAComp（周赛网站）的QQ机器人,已开源至Github:https://github.com/LEKOULEKOUHAO/SCUCACompQQbot"
    msg += "\n协会网站已开源至Github:https://github.com/Westlifers/SCUCAWeb"
    await about.finish(msg)
#---------------------------------------------------------------------------------------------#
party = on_command("impart", aliases={"party","聚会","银趴","淫趴"}, permission= GROUP, priority=1)
eat = on_command("eat", aliases={"吃"}, permission= GROUP, priority=1)
draw = on_command("draw", aliases={"抽签"}, permission= GROUP, priority=1)
reward = on_command("reward", aliases={"发奖"}, permission= GROUP, priority=1)

@party.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.party(event)
    await party.finish(msg)

@eat.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.eat(event)
    await eat.finish(msg)

@draw.handle()
async def _(event: GroupMessageEvent,args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await draw.finish("还未输入需要参加抽签的人数或选手名~")
    elif len(args) == 1 and args[0].isdigit():
        msg = SCUCABot.draw(event,int(args[0]),None)
        await draw.finish(msg)
    else:
        username_list = [args[i] for i in range(len(args))]
        msg = SCUCABot.draw(event,None,username_list)
        await draw.finish(msg)

@reward.handle()
async def _(event: GroupMessageEvent,args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await reward.finish("还未输入发奖项目和选手名~")
    elif args[0] not in CubeEvent:
        await reward.finish("请输入正确的项目名称😠" + event_tips)
    elif len(args) != 4:
        await reward.finish("输入格式错误~(使用示例:/发奖 333 李俊良 李wr 李温柔)")
    else:
        [msg1, msg2, msg3] = SCUCABot.reward(event,args[0],args[1],args[2],args[3])
        await reward.send(msg1)
        await reward.send(msg2)
        await reward.finish(msg3)
#---------------------------------------------------------------------------------------------#
pk = on_command("pk", aliases={"打架"}, permission= GROUP, priority=1)

@pk.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await pk.finish("还没输入选手名~(使用示例:/pk 张三 李四)")
    elif len(args) == 1:
        await pk.finish("还没输入另一个选手名~(使用示例:/pk 张三 李四)")
    elif len(args) > 2:
        await pk.finish("输入选手名过多~(使用示例:/pk 张三 李四)")
    
    msg = SCUCABot.pk(event,args[0],args[1])
    await pk.finish(msg)
#---------------------------------------------------------------------------------------------#
score = on_command("score", aliases={"积分榜"}, permission= GROUP, priority=1)
uestc = on_command("uestc", aliases={"沉淀值"}, permission= GROUP, priority=1)

@score.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.score(event)
    await score.finish(msg)

@uestc.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.uestc(event)
    await uestc.finish(msg)
#---------------------------------------------------------------------------------------------#
scuca = on_command("scuca", aliases={"开盒","开","盒"}, permission= GROUP, priority=1)

@scuca.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await scuca.finish("还没输入选手名~(使用示例:/scuca 张三)")

    msg = SCUCABot.scuca(event,args[0])
    await scuca.finish(msg)
#---------------------------------------------------------------------------------------------#
scur = on_command("scur", aliases={"纪录"}, permission= GROUP, priority=1)

@scur.handle()
async def _(event: GroupMessageEvent):
    msg = SCUCABot.scur(event)
    await scur.finish(msg)
#---------------------------------------------------------------------------------------------#
scurank = on_command("scurank", aliases={"总排名"}, permission= GROUP, priority=1)

@scurank.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await scurank.finish("还没输入你要查询的项目~" + event_tips)
    elif args[0] not in CubeEvent:
        await scurank.finish("请输入正确的项目名称😠" + event_tips)
    
    msg = SCUCABot.scurank(event,args[0])
    await scurank.finish(msg)
#---------------------------------------------------------------------------------------------#
travel = on_command("travel", aliases={"润"}, permission= GROUP, priority=1)

@travel.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        msg = SCUCABot.travel(event)
        await travel.finish(msg)
    else:
        #判断输入的地名里有没有错误的地名，只要有一个就返回错误提示
        for i in range(len(args)):
            if args[i] not in provincess:
                await travel.finish("请输入正确的地名（只支持省,使用示例:/润 四川）😠")
        
        province_list = [args[i] for i in range(len(args))]
        msg = SCUCABot.travel(event,province_list)
        await travel.finish(msg)
#---------------------------------------------------------------------------------------------#
weekrank = on_command("weekrank", aliases={"周排名"}, permission= GROUP, priority=1)
comprank = on_command("comprank", aliases={"比赛排名"}, permission= GROUP, priority=1)

@weekrank.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await weekrank.finish("还没输入你要查询的项目~" + event_tips)
    elif args[0] not in CubeEvent:
        await weekrank.finish("请输入正确的项目名称😠" + event_tips)

    msg = SCUCABot.weekrank(event,args[0])
    await weekrank.finish(msg)

@comprank.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await comprank.finish("还没输入你要查询的项目~" + event_tips)
    elif args[0] not in CubeEvent:
        await comprank.finish("请输入正确的项目名称😠" + event_tips)

    msg = SCUCABot.comprank(event,args[0])
    await comprank.finish(msg)
#---------------------------------------------------------------------------------------------#
weekresults = on_command("zcj", aliases={"周成绩"}, permission= GROUP, priority=1)

@weekresults.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await weekresults.finish("还没输入选手名~(使用示例:/开盒 李俊良)")
    elif len(args) > 1:
        await weekresults.finish("输入选手名过多~(使用示例:/开盒 李俊良)")
    
    msg = SCUCABot.weekresults(event,args[0])
    await weekresults.finish(msg)
#---------------------------------------------------------------------------------------------#
summary = on_command("summary", aliases={"总结"}, permission= GROUP, priority=1)

@summary.handle()
async def _(event: GroupMessageEvent):
    #判断是否为超级管理员权限
    if event.get_user_id() not in superusers:
        await summary.finish("你没有权限使用该命令哦~")
    else:
        for msg in SCUCABot.summary(event):
            await summary.send(msg)

        await summary.finish()
#---------------------------------------------------------------------------------------------#
what2pk = on_regex(r"^(/2|/3|/4|/5|/6|/7|/sq|/sk|/minx|/py|/3oh|/3bf|/4bf|/5bf|/clock)$", permission= GROUP, priority=1)

@what2pk.handle()
async def _(event: GroupMessageEvent, args = RegexMatched()):
    #msg = SCUCABot.scramble(event,event_convert2(args.group(1))) #本地用这个
    msg = SCUCABot.scramble(event,event_convert2(args)) # 服务器上用这个
    await what2pk.finish(msg)
#---------------------------------------------------------------------------------------------#
wca = on_command("wca", aliases={"官方"}, permission= GROUP, priority=1)

@wca.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await wca.finish("还未输入选手名~(使用示例:/wca 李俊良)")
    elif len(args) > 1:
        await wca.finish("输入选手名过多~(使用示例:/wca 李俊良)")

    msg = SCUCABot.wca(event,args[0])
    await wca.finish(msg)
#---------------------------------------------------------------------------------------------#
#@scheduler.scheduled_job("cron", day_of_week = "sun", hour = 20, minute = 0, misfire_grace_time = 60)
#---------------------------------------------------------------------------------------------#

class SCUCABot:
    party_flag = 1 #1表示望江，0表示江安
    
    def web(event:MessageEvent):
        msg = web_display()
        return msg

    def help(event: MessageEvent):
        msg = help_display()
        return msg

    def scur(event: MessageEvent):
        msg = record_display()
        return msg
    
    def scuca(event: MessageEvent, username:str):
        msg = scuca_display(username)
        return msg

    def weekrank(event: MessageEvent, cubeevent:str):
        if(response_week_ongoing() == 0):
            msg = "当前没有正在进行的周赛！"
        else:
            msg = week_display(cubeevent)

        return msg
    
    def comprank(event: MessageEvent, cubeevent:str):
        if (response_special_ongoing() == 0):
            msg = "当前没有正在进行的正式比赛！"
        else:
            msg = spec_display(cubeevent)
        return msg
    
    def scurank(event: MessageEvent, cubeevent:str):
        msg = top10_display(cubeevent)
        return msg
    
    def pk(event: MessageEvent, username1:str, username2:str):
        msg = pk_display(username1,username2)
        return msg
    
    def weekresults(event: MessageEvent, username:str):
        msg = week_results_display(username)
        return msg

    def score(event: MessageEvent):
        msg = score_display()
        return msg
    
    def uestc(event: MessageEvent):
        msg = uestc_display()
        return msg
    
    def summary(event: MessageEvent):
        msg = summary_display()
        return msg

    def party(event: MessageEvent):
        [msg, SCUCABot.party_flag] = party_display()
        return msg
    
    def eat(event: MessageEvent):
        msg = eat_display(SCUCABot.party_flag)
        return msg
    
    def draw(event: MessageEvent, num = None, username_list = None):
        msg = draw_display(num, username_list)
        return msg
 
    def reward(event: MessageEvent, cubeevent: str, username1, username2, username3):
        msg = reward_display(cubeevent, username1, username2, username3)
        return msg

    def travel(event: MessageEvent, province_list = None):
        msg = travel_display(province_list)
        return msg
    
    def scramble(event: MessageEvent,cubeevent:str):
        msg = scramble_display(cubeevent)
        return msg
    
    def wca(event: MessageEvent, wca_id:str):
        msg = wca_display(wca_id)
        return msg