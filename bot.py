#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

# 自定义日志配置（可选）
# 
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# 初始化 Nonebot
nonebot.init()
app = nonebot.get_asgi()

# 获取驱动器并注册适配器
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

# 加载内置插件
nonebot.load_builtin_plugins("echo")

# 从 pyproject.toml 加载插件
nonebot.load_from_toml("pyproject.toml")

# 修改配置（可选）
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
