import nonebot

nonebot.require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler


# 每周日20:00执行
@scheduler.scheduled_job("cron", day_of_week='sun', hour='20', minute='0', second='0', id="job_0")
async def run_weekly():
    bot = nonebot.get_bot()
    # await bot.send_msg(message_type="group", group_id=231447662, message="每周日20:00跑")
