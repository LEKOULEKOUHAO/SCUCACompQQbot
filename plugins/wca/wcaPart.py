from plugins.scur.data_source import wca_url
from plugins.scur.utils import response

def key2event(key):
    match key:
        case '3x3x3 Cube':
            return '333'
        case '2x2x2 Cube':
            return '222'
        case '4x4x4 Cube':
            return '444'
        case '5x5x5 Cube':
            return '555'
        case '6x6x6 Cube':
            return '666'
        case '7x7x7 Cube':
            return '777'
        case '3x3x3 Blindfolded':
            return '333bf'
        case '3x3x3 Fewest Moves':
            return '333fm'
        case '3x3x3 One-Handed':
            return '333oh'
        case 'Clock':
            return 'clock'
        case 'Megaminx':
            return 'minx'
        case 'Pyraminx':
            return 'pyram'
        case 'Skewb':
            return 'skewb'
        case 'Square-1':
            return 'sq1'
        case '4x4x4 Blindfolded':
            return '444bf'
        case '5x5x5 Blindfolded':
            return '555bf'
        case '3x3x3 Multi-Blind':
            return '333mbf'
        case _:
            return 'unknown'

def wca_display(wca_id):
    url = wca_url(wca_id)
    try :
        l = response(url)
    except:
        return '查询失败,请检查所输入WCA ID是否正确~'
    msg = ''
    l = l['person']
    u_name = l['name']
    msg += f'{u_name}(WCA ID: {wca_id})的WCA官方成绩如下:'
    msg += '\n项目  单次  ||  平均'
    grades_dict = l['personalRecords']
    keys_list = list(grades_dict.keys())
    values_list = [[grades_dict[key] for key in keys_list]]
    grades_dict = values_list[0]
    for i in grades_dict:
        if i['average']['time'] != '':
            msg += '\n' + key2event(i['event']) + '  ' +  i['single']['time'] + '  ||  ' + i['average']['time']
        else:
            msg += '\n' + key2event(i['event']) + '  ' +  i['single']['time'] + '  ||  ' + '--'

    return msg


