import nonebot

from ..utils import response

nonebot.require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler


# 每天8:00执行
@scheduler.scheduled_job("cron", hour='8', minute='0', second='0', id="job_0")
async def run_weekly():
    bot = nonebot.get_bot()
    scrambles = response('http://localhost:2020/scramble/333?numberOfScrambles=5')['scrambles']

    message = '起床做题：\n\n' + '\n\n'.join([f'{i+1}. ' + s for i, s in enumerate(scrambles)])

    # await bot.send_msg(message_type="group", group_id=783204511, message=message)
    await bot.send_msg(message_type="group", group_id=980371417, message=message)
