import random

from .data_source import provincess, cities

def travel_display(province_list = None):
    if province_list == None:
            province = random.choice(provincess)
            for i in cities:
                if i['name'] == province:
                    r = random.choice(i['cities'])

    else:
        province = random.choice(province_list)
        for i in cities:
            if i['name'] == province:
                r = random.choice(i['cities'])

    if province == '北京' or province == '上海' or province == '天津' or province == '重庆':
        msg = f'去{r}吧！'
    else:
        msg = f'去{province}的{r}吧！'

    return msg

