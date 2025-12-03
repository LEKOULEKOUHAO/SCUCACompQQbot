from nonebot.adapters.onebot.v11 import MessageSegment
import os
import base64

from .scucaPart import response_userdata
from .data_source import CubeEvent, pkCompareAvgEvent, pkCompareBestEvent, _font_path
from .utils import create_table, time_convert


def _compare_scores(score1, score2):
    """比较两个成绩，返回胜负情况"""
    if score1 > 0 and score2 > 0:
        if score1 < score2:
            return 1, 0  # 第一个选手赢
        elif score1 > score2:
            return 0, 1  # 第二个选手赢
        else:
            return 0, 0  # 平局
    elif score1 > 0 and score2 == 0:
        return 1, 0
    elif score1 == 0 and score2 > 0:
        return 0, 1
    else:
        return 0, 0


def _add_comparison_result(result_list, username1, username2, event, score1, score2, is_best=False):
    """
    添加比较结果到列表
    
    Args:
        result_list: 结果列表
        username1, username2: 两个选手的名字
        event: 项目
        score1, score2: 成绩
        is_best: 是否为单次成绩（True）或平均成绩（False）
    """
    win1, win2 = _compare_scores(score1, score2)
    
    result_list.append({
        'username': username1,
        'event': event,
        'avg': score1,
        'win': win1
    })
    result_list.append({
        'username': username2,
        'event': event,
        'avg': score2,
        'win': win2
    })


def _process_event_data(result_list, records1, records2, event_list, username1, username2):
    """
    处理相同和不同的事件数据
    
    处理两个选手都有的项目，以及只有一个选手有的项目
    """
    # 处理两个选手都有的项目
    for record1 in records1:
        for record2 in records2:
            if record1['event'] == record2['event']:
                score_key = 'avg' if 'avg' in record1 else 'best'
                _add_comparison_result(
                    result_list, username1, username2, record1['event'],
                    record1[score_key], record2[score_key]
                )
                break
    
    # 处理只有选手1有的项目
    for record1 in records1:
        if not any(r['event'] == record1['event'] for r in records2):
            score_key = 'avg' if 'avg' in record1 else 'best'
            if record1[score_key] != 0:
                result_list.append({
                    'username': username1,
                    'event': record1['event'],
                    'avg': record1[score_key],
                    'win': 1
                })
                result_list.append({
                    'username': username2,
                    'event': record1['event'],
                    'avg': '--',
                    'win': 0
                })
    
    # 处理只有选手2有的项目
    for record2 in records2:
        if not any(r['event'] == record2['event'] for r in records1):
            score_key = 'avg' if 'avg' in record2 else 'best'
            if record2[score_key] != 0:
                result_list.append({
                    'username': username1,
                    'event': record2['event'],
                    'avg': '--',
                    'win': 0
                })
                result_list.append({
                    'username': username2,
                    'event': record2['event'],
                    'avg': record2[score_key],
                    'win': 1
                })


def pklist(u1: str, u2: str):
    """
    给出两个选手的PK数据列表
    
    Args:
        u1: 选手1
        u2: 选手2
    
    Returns:
        list: PK数据列表或错误代码
            -4: 选手名输入有误
            -3: u1无成绩
            -2: u2无成绩
            -1: 两个选手都无成绩
            0: 两个选手相同
            list: PK数据列表
    """
    r1 = response_userdata(u1)
    r2 = response_userdata(u2)
    
    if r1 == -1 or r2 == -1:
        return -4
    elif r1 == 0 and r2 != 0:
        return -3
    elif r2 == 0 and r1 != 0:
        return -2
    elif r1 == 0 and r2 == 0:
        return -1
    elif r1 == r2:
        return 0
    
    result = []
    
    # 处理平均成绩
    r1_avg = [i for i in r1['avg'] if i['event'] in pkCompareAvgEvent]
    r2_avg = [i for i in r2['avg'] if i['event'] in pkCompareAvgEvent]
    _process_event_data(result, r1_avg, r2_avg, pkCompareAvgEvent, u1, u2)
    
    # 处理单次成绩
    r1_best = [i for i in r1['best'] if i['event'] in pkCompareBestEvent]
    r2_best = [i for i in r2['best'] if i['event'] in pkCompareBestEvent]
    _process_event_data(result, r1_best, r2_best, pkCompareBestEvent, u1, u2)
    
    return result


def _get_score_display(score1, score2, username1, username2):
    """根据分差返回比赛结果描述"""
    diff = abs(score1 - score2)
    if score1 > score2:
        winner = username1
        loser = username2
        if diff < 3:
            result = f"(小赢！){winner}"
        elif diff < 6:
            result = f"(中赢！){winner}"
        elif diff < 9:
            result = f"(大赢！){winner}"
        else:
            result = f"(赢麻！){winner}"
        return winner, f"{score1} : {score2}", result
    elif score1 < score2:
        if diff < 3:
            result = f"(小赢！){username2}"
        elif diff < 6:
            result = f"(中赢！){username2}"
        elif diff < 9:
            result = f"(大赢！){username2}"
        else:
            result = f"(赢麻！){username2}"
        return username1, f"{score1} : {score2}", result
    else:
        return username1, f"{score1} : {score2}双赢！", username2


def pk_display(u1: str, u2: str):
    """
    PK的展示函数
    
    Args:
        u1: 选手1
        u2: 选手2
    
    Returns:
        str或MessageSegment: PK结果
    """
    pk_list = pklist(u1, u2)
    
    # 处理错误情况
    error_messages = {
        -4: "输入选手名有误~",
        -3: f"{u1}暂无SCUCA官方成绩~",
        -2: f"{u2}暂无SCUCA官方成绩~",
        -1: f"{u1}和{u2}暂无SCUCA官方成绩~",
        0: "别在这理发店😠",
    }
    
    if pk_list in error_messages:
        return error_messages[pk_list]
    
    # 构建表格
    pk_list.sort(key=lambda x: CubeEvent.index(x['event']))
    msg = [[u1, 'VS', u2]]
    
    score1 = 0
    score2 = 0
    
    for r in range(0, len(pk_list), 2):
        player1 = pk_list[r]
        player2 = pk_list[r + 1]
        
        if player1['win'] == 1 and player2['win'] == 0:
            score1 += 1
            score_str2 = player2['avg'] if player2['avg'] == '--' else time_convert(player2['avg'])
            msg.append([f"{time_convert(player1['avg'])}(赢！)", player1['event'], score_str2])
        elif player1['win'] == 0 and player2['win'] == 1:
            score2 += 1
            score_str1 = player1['avg'] if player1['avg'] == '--' else time_convert(player1['avg'])
            msg.append([score_str1, player1['event'], f"{time_convert(player2['avg'])}(赢！)"])
        else:
            score_str1 = time_convert(player1['avg']) if player1['avg'] != '--' else '--'
            score_str2 = time_convert(player2['avg']) if player2['avg'] != '--' else '--'
            msg.append([score_str1, player1['event'], score_str2])
    
    # 添加最终结果
    p1, score_display, p2 = _get_score_display(score1, score2, u1, u2)
    msg.append([p1, score_display, p2])
    
    # 生成图片
    row = len(msg)
    img = create_table(800, 80 * row, _font_path, 30, row, 3, msg, [], [0, 1, 2])
    img.save('pk.png')
    
    with open('pk.png', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    img = MessageSegment.image('base64://' + encoded_image)
    os.remove('pk.png')
    
    return img


