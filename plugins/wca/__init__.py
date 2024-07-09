from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, GROUP, Message

from .cubingSearch import *
from .fetchDetail import *

wca = on_command("wca", aliases={"官方"}, permission=GROUP, priority=1)
wr = on_command("wr", aliases={"纪录"}, permission=GROUP, priority=1)

def getWcaResult(nameOrId: str) -> str:
    searchResult = fetchSearchResult(nameOrId)

    if len(searchResult) == 0:
        return "未找到符合条件的选手"
    elif len(searchResult) > 1:
        rep = "找到多个符合条件的选手\n"
        for person in searchResult:
            rep += f'{person[0]} [{person[1]}]\n'
        if len(searchResult) == 10:
            rep += '......\n'
        rep += '请提供更多信息以缩小范围'
        return rep
    else:
        detail = fetchUserDetail(searchResult[0][1])
        personalRecords = detail['personalRecords']
        rep = f'{searchResult[0][0]}({searchResult[0][1]})\n'
        rep += '项目  单次  ||  平均'

        for (event, time) in personalRecords.items():
            rep += f'\n{event}  {time["single"]["time"]}  ||  {time["average"]["time"] if time["average"]["time"] else "--"}'
        return rep


@wca.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await wca.finish("还未输入wcaid~(使用示例:/wca 2023LIYA04)")
    elif len(args) > 1:
        await wca.finish("输入wcaid过多~(使用示例:/wca 2023LIYA04)")

    msg = getWcaResult(args[0])
    await wca.finish(msg)


def getWRResult(includeOld: bool) -> str:
    data = fetchWR(includeOld)
    rep = "世界 综合 记录\n单次 平均\n"
    for event in data:
        try:
            rep += f'{event["event"]} {event["single"][0]["player"] + " " + event["single"][0]["time"] if event["single"][0] else "-"} || {event["average"][0]["player"] + " " + event["average"][0]["time"] if event["average"] else "-"}\n'
        except:
            print(event)
    return rep


@wr.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    include_old = False
    if len(args) > 1:
        await wr.finish("输入参数过多")
    elif len(args) == 1:
        include_old = True

    msg = getWRResult(include_old)
    await wr.finish(msg)
