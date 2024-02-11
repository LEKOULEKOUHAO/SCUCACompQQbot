from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, GROUP, Message

from plugins.wca.cubingSearch import fetchSearchResult
from plugins.wca.fetchDetail import fetchDetail

wca = on_command("wca", aliases={"官方"}, permission=GROUP, priority=1)

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
        detail = fetchDetail(searchResult[0][1])
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