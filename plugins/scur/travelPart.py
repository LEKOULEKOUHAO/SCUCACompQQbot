import random

from .data_source import provincess, cities


def _find_city_in_province(province: str) -> str:
    """在城市列表中查找省份并随机返回一个城市"""
    for province_data in cities:
        if province_data['name'] == province:
            return random.choice(province_data['cities'])
    return ""


def _format_travel_message(province: str, city: str) -> str:
    """格式化旅游消息"""
    # 直辖市和直属城市直接显示城市名
    direct_controlled = {'北京', '上海', '天津', '重庆'}
    if province in direct_controlled:
        return f'去{city}吧！'
    return f'去{province}的{city}吧！'


def travel_display(province_list=None):
    """
    随机选择旅游地点
    
    Args:
        province_list: 可选的省份列表，若为None则从所有省份中随机选择
    
    Returns:
        str: 旅游建议消息
    """
    # 选择省份
    provinces_to_choose = province_list if province_list else provincess
    province = random.choice(provinces_to_choose)
    
    # 找到对应省份的城市
    city = _find_city_in_province(province)
    
    # 格式化消息
    return _format_travel_message(province, city)


