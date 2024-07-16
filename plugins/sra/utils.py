import requests
import json

#从接口请求数据,处理为json
def response(url:str):
    #尝试从接口请求数据，若失败则返回错误信息
    try:
        response = requests.post(url).text
        response_json = json.loads(response)

    except:
        response_json = {'code':99999}

    return response_json
    
#录入规则：123456代表，12:34.56，11234代表1：12.34，1234代表12.34
def time_convert(time:int):
    if time != 999999 and time != 'dnf' and time != 'dns' and time != 'DNS' and time != 'DNF':
        time = str(time)
        if len(time) == 6:
            time = time[0:2] + ':' + time[2:4] + '.' + time[4:6]
        elif len(time) == 5:
            time = time[0] + ':' + time[1:3] + '.' + time[3:5]
        elif len(time) == 4:
            time = time[0:2] + '.' + time[2:4]
        elif len(time) == 3:
            time = time[0] + '.' + time[1:3]
    
    else:
        time = 'DNF'

    return time
   
def e_id2event(e_id:int):
    match e_id:
        case 1:
            event = '333'
        case 2:
            event = '222'
        case 3:
            event = '444'
        case 4:
            event = '555'
        case 5:
            event = '666'
        case 6:
            event = '777'
        case 7:
            event = '333oh'
        case 8:
            event = 'pyram'
        case 9:
            event = 'skewb'
        case 10:
            event = 'minx'
        case 11:
            event = '333bf'
        case 12:
            event = '444bf'
        case 13:
            event = '555bf'
        case 14:
            event = '333mbf'
        case 15:
            event = 'sq1'
        case 16:
            event = '333fm'
        case 17:
            event = 'clock'
        case 41:
            event = 'e-333'
        case 42:
            event = 'e-333oh'

    return event

def event2e_id(event:str):
    match event:
        case '333':
            e_id = 1
        case '222':
            e_id = 2
        case '444':
            e_id = 3
        case '555':
            e_id = 4
        case '666':
            e_id = 5
        case '777':
            e_id = 6
        case '333oh':
            e_id = 7
        case 'pyram':
            e_id = 8
        case 'skewb':
            e_id = 9
        case 'minx':
            e_id = 10
        case '333bf':
            e_id = 11
        case '444bf':
            e_id = 12
        case '555bf':
            e_id = 13
        case '333mbf':
            e_id = 14
        case 'sq1':
            e_id = 15
        case '333fm':
            e_id = 16
        case 'clock':
            e_id = 17
        case 'e-333':
            e_id = 41
        case 'e-333oh':
            e_id = 42
        case _:
            e_id = 0

    return e_id

def rank_title(eventInput:str):
    match eventInput:
        case "222":
            msg = '二阶速拧  One  Top10'
        case "333":
            msg = '三阶速拧  One  Top10'
        case "444":
            msg = '四阶速拧  One  Top10'
        case "555":
            msg = '五阶速拧  One  Top10'
        case "666":
            msg = '六阶速拧  One  Top10'
        case "777":
            msg = '七阶速拧  One  Top10'
        case "333oh":
            msg = '三阶单手  One  Top10'
        case "333bf":
            msg = '三阶盲拧  One  Top10'
        case "333mbf":
            msg = '三阶多盲  One  Top10'
        case "pyram":
            msg = '金字塔  One  Top10'
        case "skewb":
            msg = '斜转  One  Top10'
        case "minx":
            msg = '五魔方  One  Top10'
        case "sq1":
            msg = 'SQ1  One  Top10'
        case "clock":
            msg = '魔表  One  Top10'
        case "333fm":
            msg = '三阶最少步  One  Top10'
        case "e-333":
            msg = '智能三阶  One  Top10'
        case "e-333oh":
            msg = '智能单手  One  Top10'
        case "444bf":
            msg = '四阶盲拧  One  Top10'
        case "555bf":
            msg = '五阶盲拧  One  Top10'

    return msg
    