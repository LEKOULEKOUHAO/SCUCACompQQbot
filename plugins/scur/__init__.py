from nonebot import on_command, on_notice, on_regex
from nonebot.typing import T_State
from nonebot.params import CommandArg, RegexMatched
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, GroupIncreaseNoticeEvent, Bot, GROUP, Message
from .scheduler import *

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
from .data_source import event_tips, CubeEvent, provincess, superusers
from .utils import response, event_convert2


# ======================== 命令定义 ========================
welcome = on_notice()
web = on_command("web", aliases={"网站"}, permission=GROUP, priority=1)
help = on_command("help", aliases={"帮助"}, permission=GROUP, priority=1)
about = on_command("about", aliases={"关于"}, permission=GROUP, priority=1)

party = on_command("impart", aliases={"party", "聚会", "银趴", "淫趴"}, permission=GROUP, priority=1)
eat = on_command("eat", aliases={"吃"}, permission=GROUP, priority=1)
draw = on_command("draw", aliases={"抽签"}, permission=GROUP, priority=1)
reward = on_command("reward", aliases={"发奖"}, permission=GROUP, priority=1)

pk = on_command("pk", aliases={"打架"}, permission=GROUP, priority=1)

score = on_command("score", aliases={"积分榜"}, permission=GROUP, priority=1)
uestc = on_command("uestc", aliases={"沉淀值"}, permission=GROUP, priority=1)

scuca = on_command("scuca", aliases={"开盒", "开", "盒"}, permission=GROUP, priority=1)
scur = on_command("scur", aliases={"纪录"}, permission=GROUP, priority=1)
scurank = on_command("scurank", aliases={"总排名"}, permission=GROUP, priority=1)

travel = on_command("travel", aliases={"润"}, permission=GROUP, priority=1)

weekrank = on_command("weekrank", aliases={"周排名"}, permission=GROUP, priority=1)
comprank = on_command("comprank", aliases={"比赛排名"}, permission=GROUP, priority=1)

weekresults = on_command("zcj", aliases={"周成绩"}, permission=GROUP, priority=1)
summary = on_command("summary", aliases={"总结"}, permission=GROUP, priority=1)

what2pk = on_regex(r"^(/2|/3|/4|/5|/6|/7|/sq|/sk|/minx|/py|/3oh|/3bf|/4bf|/5bf|/clock)$", permission=GROUP, priority=1)


# ======================== 欢迎和帮助命令 ========================
@welcome.handle()
async def welcome_handler(bot: Bot, event: GroupIncreaseNoticeEvent, state: T_State):
    user_id = event.get_user_id()
    at_str = f"欢迎[CQ:at,qq={user_id}]"
    msg1 = at_str + '加入🥳\n'
    msg1 += "社团网站为: https://scu.yougi.top/,若要在社团网站注册账号,请实名注册,注册后请在群里告知网站管理员后台审核通过🥰"
    msg1 = Message(msg1)
    msg2 = SCUCABot.help(event)
    await bot.send(event, msg1)
    await bot.send(event, msg2)


@help.handle()
async def help_handler(event: GroupMessageEvent):
    msg = SCUCABot.help(event)
    await help.finish(msg)


@web.handle()
async def web_handler(event: GroupMessageEvent):
    msg = SCUCABot.web(event)
    await web.finish(msg)


@about.handle()
async def about_handler(event: GroupMessageEvent):
    msg = "本项目为四川大学魔方协会SCUCAComp（周赛网站）的QQ机器人,已开源至Github:https://github.com/LEKOULEKOUHAO/SCUCACompQQbot"
    msg += "\n协会网站已开源至Github:https://github.com/Westlifers/SCUCAWeb"
    await about.finish(msg)


# ======================== 聚会、吃饭、抽签、发奖命令 ========================
@party.handle()
async def party_handler(event: GroupMessageEvent):
    msg = SCUCABot.party(event)
    await party.finish(msg)


@eat.handle()
async def eat_handler(event: GroupMessageEvent):
    msg = SCUCABot.eat(event)
    await eat.finish(msg)


@draw.handle()
async def draw_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not parsed_args:
        await draw.finish("还未输入需要参加抽签的人数或选手名~")
    elif len(parsed_args) == 1 and parsed_args[0].isdigit():
        msg = SCUCABot.draw(event, int(parsed_args[0]), None)
        await draw.finish(msg)
    else:
        msg = SCUCABot.draw(event, None, parsed_args)
        await draw.finish(msg)


@reward.handle()
async def reward_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not parsed_args:
        await reward.finish("还未输入发奖项目和选手名~")
    elif parsed_args[0] not in CubeEvent:
        await reward.finish("请输入正确的项目名称😠" + event_tips)
    elif len(parsed_args) != 4:
        await reward.finish("输入格式错误~(使用示例:/发奖 333 选手1 选手2 选手3)")
    else:
        result_images = SCUCABot.reward(event, parsed_args[0], parsed_args[1], parsed_args[2], parsed_args[3])
        for img in result_images:
            await reward.send(img)
        await reward.finish()


# ======================== PK命令 ========================
@pk.handle()
async def pk_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not parsed_args:
        await pk.finish("还没输入选手名~(使用示例:/pk 张三 李四)")
    elif len(parsed_args) == 1:
        await pk.finish("还没输入另一个选手名~(使用示例:/pk 张三 李四)")
    elif len(parsed_args) > 2:
        await pk.finish("输入选手名过多~(使用示例:/pk 张三 李四)")
    
    msg = SCUCABot.pk(event, parsed_args[0], parsed_args[1])
    await pk.finish(msg)


# ======================== 积分和排名命令 ========================
@score.handle()
async def score_handler(event: GroupMessageEvent):
    msg = SCUCABot.score(event)
    await score.finish(msg)


@uestc.handle()
async def uestc_handler(event: GroupMessageEvent):
    msg = SCUCABot.uestc(event)
    await uestc.finish(msg)


# ======================== 选手查询命令 ========================
@scuca.handle()
async def scuca_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not parsed_args:
        await scuca.finish("还没输入选手名~(使用示例:/scuca 张三)")
    msg = SCUCABot.scuca(event, parsed_args[0])
    await scuca.finish(msg)


@scur.handle()
async def scur_handler(event: GroupMessageEvent):
    msg = SCUCABot.scur(event)
    await scur.finish(msg)


def _validate_event(event_name: str, command_name: str) -> bool:
    """验证事件名称是否有效"""
    if not event_name:
        return False
    if event_name not in CubeEvent:
        return False
    return True


@scurank.handle()
async def scurank_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not _validate_event(parsed_args[0] if parsed_args else "", "scurank"):
        await scurank.finish("还没输入你要查询的项目~" + event_tips)
    msg = SCUCABot.scurank(event, parsed_args[0])
    await scurank.finish(msg)


# ======================== 旅游命令 ========================
@travel.handle()
async def travel_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not parsed_args:
        msg = SCUCABot.travel(event)
        await travel.finish(msg)
    
    # 验证所有地名
    invalid_provinces = [arg for arg in parsed_args if arg not in provincess]
    if invalid_provinces:
        await travel.finish("请输入正确的地名（只支持省,使用示例:/润 四川）😠")
    
    msg = SCUCABot.travel(event, parsed_args)
    await travel.finish(msg)


# ======================== 周赛和比赛命令 ========================
@weekrank.handle()
async def weekrank_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not _validate_event(parsed_args[0] if parsed_args else "", "weekrank"):
        await weekrank.finish("还没输入你要查询的项目~" + event_tips)
    msg = SCUCABot.weekrank(event, parsed_args[0])
    await weekrank.finish(msg)


@comprank.handle()
async def comprank_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not _validate_event(parsed_args[0] if parsed_args else "", "comprank"):
        await comprank.finish("还没输入你要查询的项目~" + event_tips)
    msg = SCUCABot.comprank(event, parsed_args[0])
    await comprank.finish(msg)


@weekresults.handle()
async def weekresults_handler(event: GroupMessageEvent, args: Message = CommandArg()):
    parsed_args = args.extract_plain_text().strip().split()
    if not parsed_args:
        await weekresults.finish("还没输入选手名~(使用示例:/zcj 张三)")
    elif len(parsed_args) > 1:
        await weekresults.finish("输入选手名过多~(使用示例:/zcj 张三)")
    
    msg = SCUCABot.weekresults(event, parsed_args[0])
    await weekresults.finish(msg)


# ======================== 总结命令 ========================
@summary.handle()
async def summary_handler(event: GroupMessageEvent):
    if event.get_user_id() not in superusers:
        await summary.finish("你没有权限使用该命令哦~")
    
    for msg in SCUCABot.summary(event):
        await summary.send(msg)
    await summary.finish()


# ======================== 打乱命令 ========================
@what2pk.handle()
async def scramble_handler(event: GroupMessageEvent, args=RegexMatched()):
    msg = SCUCABot.scramble(event, event_convert2(args))
    await what2pk.finish(msg)


# ======================== 机器人核心类 ========================
class SCUCABot:
    """SCUCA机器人核心业务逻辑类"""
    party_flag = 1  # 1表示望江，0表示江安
    
    @staticmethod
    def web(event: MessageEvent):
        return web_display()

    @staticmethod
    def help(event: MessageEvent):
        return help_display()

    @staticmethod
    def scur(event: MessageEvent):
        return record_display()
    
    @staticmethod
    def scuca(event: MessageEvent, username: str):
        return scuca_display(username)

    @staticmethod
    def weekrank(event: MessageEvent, cubeevent: str):
        if response_week_ongoing() == 0:
            return "当前没有正在进行的周赛！"
        return week_display(cubeevent)
    
    @staticmethod
    def comprank(event: MessageEvent, cubeevent: str):
        if response_special_ongoing() == 0:
            return "当前没有正在进行的正式比赛！"
        return spec_display(cubeevent)
    
    @staticmethod
    def scurank(event: MessageEvent, cubeevent: str):
        return top10_display(cubeevent)
    
    @staticmethod
    def pk(event: MessageEvent, username1: str, username2: str):
        return pk_display(username1, username2)
    
    @staticmethod
    def weekresults(event: MessageEvent, username: str):
        return week_results_display(username)

    @staticmethod
    def score(event: MessageEvent):
        return score_display()
    
    @staticmethod
    def uestc(event: MessageEvent):
        return uestc_display()
    
    @staticmethod
    def summary(event: MessageEvent):
        return summary_display()

    @staticmethod
    def party(event: MessageEvent):
        msg, SCUCABot.party_flag = party_display()
        return msg
    
    @staticmethod
    def eat(event: MessageEvent):
        return eat_display(SCUCABot.party_flag)
    
    @staticmethod
    def draw(event: MessageEvent, num=None, username_list=None):
        return draw_display(num, username_list)
 
    @staticmethod
    def reward(event: MessageEvent, cubeevent: str, username1: str, username2: str, username3: str):
        return reward_display(cubeevent, username1, username2, username3)

    @staticmethod
    def travel(event: MessageEvent, province_list=None):
        return travel_display(province_list)
    
    @staticmethod
    def scramble(event: MessageEvent, cubeevent: str):
        return scramble_display(cubeevent)

