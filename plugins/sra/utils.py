import requests
import json
import logging

logger = logging.getLogger(__name__)


def response(url: str) -> dict:
    """
    从接口请求数据，处理为JSON格式
    
    若失败则返回错误代码 99999
    """
    try:
        response_text = requests.post(url).text
        return json.loads(response_text)
    except Exception as e:
        logger.error(f"Failed to fetch data from {url}: {e}")
        return {'code': 99999}


# 时间记录规则：123456代表 12:34.56，11234代表 1:12.34，1234代表 12.34
TIME_FORMAT_MAP = {
    6: lambda t: f"{t[0:2]}:{t[2:4]}.{t[4:6]}",
    5: lambda t: f"{t[0]}:{t[1:3]}.{t[3:5]}",
    4: lambda t: f"{t[0:2]}.{t[2:4]}",
    3: lambda t: f"{t[0]}.{t[1:3]}",
}

DNF_VALUES = {999999, 'dnf', 'dns', 'DNS', 'DNF'}


def time_convert(time_value) -> str:
    """将整数时间转换为标准格式字符串"""
    if time_value in DNF_VALUES:
        return 'DNF'
    
    time_str = str(time_value)
    length = len(time_str)
    
    if length in TIME_FORMAT_MAP:
        return TIME_FORMAT_MAP[length](time_str)
    
    return str(time_value)


# 事件ID与事件代码的映射
EVENT_ID_MAP = {
    1: '333',
    2: '222',
    3: '444',
    4: '555',
    5: '666',
    6: '777',
    7: '333oh',
    8: 'pyram',
    9: 'skewb',
    10: 'minx',
    11: '333bf',
    12: '444bf',
    13: '555bf',
    14: '333mbf',
    15: 'sq1',
    16: '333fm',
    17: 'clock',
    41: 'e-333',
    42: 'e-333oh',
}

# 反向映射
EVENT_CODE_MAP = {v: k for k, v in EVENT_ID_MAP.items()}


def e_id2event(e_id: int) -> str:
    """将事件ID转换为事件代码"""
    return EVENT_ID_MAP.get(e_id, 'unknown')


def event2e_id(event: str) -> int:
    """将事件代码转换为事件ID"""
    return EVENT_CODE_MAP.get(event, 0)


# 事件显示标题映射
RANK_TITLE_MAP = {
    "222": "二阶速拧  One  Top10",
    "333": "三阶速拧  One  Top10",
    "444": "四阶速拧  One  Top10",
    "555": "五阶速拧  One  Top10",
    "666": "六阶速拧  One  Top10",
    "777": "七阶速拧  One  Top10",
    "333oh": "三阶单手  One  Top10",
    "333bf": "三阶盲拧  One  Top10",
    "333mbf": "三阶多盲  One  Top10",
    "pyram": "金字塔  One  Top10",
    "skewb": "斜转  One  Top10",
    "minx": "五魔方  One  Top10",
    "sq1": "SQ1  One  Top10",
    "clock": "魔表  One  Top10",
    "333fm": "三阶最少步  One  Top10",
    "e-333": "智能三阶  One  Top10",
    "e-333oh": "智能单手  One  Top10",
    "444bf": "四阶盲拧  One  Top10",
    "555bf": "五阶盲拧  One  Top10",
}


def rank_title(event: str) -> str:
    """获取排名标题"""
    return RANK_TITLE_MAP.get(event, f"{event}  One  Top10")

    