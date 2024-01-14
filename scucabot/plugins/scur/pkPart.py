from nonebot.adapters.onebot.v11 import MessageSegment
import os

from .scucaPart import response_userdata
from .data_source import CubeEvent, pkCompareAvgEvent, pkCompareBestEvent, _font_path
from .utils import create_table, time_convert

#给出一个两选手pk数据的列表, u1:选手1, u2:选手2
def pklist(u1:str,u2:str):
    l= []
    r1 = response_userdata(u1)
    r2 = response_userdata(u2)
    if(r1 == -1 or r2 == -1):
        return -4
    elif(r1 == 0 and r2 != 0):
        return -3
    elif(r2 == 0 and r1 != 0):
        return -2
    elif(r1 ==0 and r2 == 0):
        return -1
    elif(r1 == r2):
        return 0
    else:
        #从r1['avg']和r2['avg']中过滤出pkCompareAvgEvent中的项目
        r1['avg'] = [i for i in r1['avg'] if i['event'] in pkCompareAvgEvent]
        r2['avg'] = [i for i in r2['avg'] if i['event'] in pkCompareAvgEvent]
        for i in r1['avg']:
            for j in r2['avg']:
                if(i['event'] == j['event']):
                    if(i['avg'] > 0 and j['avg'] > 0 and i['avg'] < j['avg']):
                        l.append({'username':u1,'event':i['event'],'avg':i['avg'],'win':1})
                        l.append({'username':u2,'event':j['event'],'avg':j['avg'],'win':0})

                    elif(i['avg'] > 0 and j['avg'] > 0 and i['avg'] > j['avg']):
                        l.append({'username':u1,'event':i['event'],'avg':i['avg'],'win':0})
                        l.append({'username':u2,'event':j['event'],'avg':j['avg'],'win':1})

                    elif(i['avg'] > 0 and j['avg'] > 0 and i['avg'] == j['avg']):
                        l.append({'username':u1,'event':i['event'],'avg':i['avg'],'win':0})
                        l.append({'username':u2,'event':j['event'],'avg':j['avg'],'win':0})

                    elif(i['avg'] == 0 and j['avg'] > 0):
                        l.append({'username':u1,'event':i['event'],'avg':'--','win':0})
                        l.append({'username':u2,'event':j['event'],'avg':j['avg'],'win':1})

                    elif(i['avg'] > 0 and j['avg'] == 0):
                        l.append({'username':u1,'event':i['event'],'avg':i['avg'],'win':1})
                        l.append({'username':u2,'event':j['event'],'avg':'--','win':0})

        for i in r1['avg']:
            flag = 0
            for j in r2['avg']:
                if(i['event'] == j['event']):
                    flag = 1
            if(flag == 0):
                if(i['avg'] != 0):
                    l.append({'username':u1,'event':i['event'],'avg':i['avg'],'win':1})
                    l.append({'username':u2,'event':i['event'],'avg':'--','win':0})

        for i in r2['avg']:
            flag = 0
            for j in r1['avg']:
                if(i['event'] == j['event']):
                    flag = 1
            if(flag == 0):
                if(i['avg'] != 0):
                    l.append({'username':u1,'event':i['event'],'avg':'--','win':0})
                    l.append({'username':u2,'event':i['event'],'avg':i['avg'],'win':1})

        #从r1['best']和r2['best']中过滤出pkCompareBestEvent中的项目
        r1['best'] = [i for i in r1['best'] if i['event'] in pkCompareBestEvent]
        r2['best'] = [i for i in r2['best'] if i['event'] in pkCompareBestEvent]
        for i in r1['best']:
            for j in r2['best']:
                if(i['event'] == j['event']):
                    if(i['best'] > 0 and j['best'] > 0 and i['best'] < j['best']):
                        l.append({'username':u1,'event':i['event'],'avg':i['best'],'win':1})
                        l.append({'username':u2,'event':j['event'],'avg':j['best'],'win':0})

                    elif(i['best'] > 0 and j['best'] > 0 and i['best'] > j['best']):
                        l.append({'username':u1,'event':i['event'],'avg':i['best'],'win':0})
                        l.append({'username':u2,'event':j['event'],'avg':j['best'],'win':1})

                    elif(i['best'] > 0 and j['best'] > 0 and i['best'] == j['best']):
                        l.append({'username':u1,'event':i['event'],'avg':i['best'],'win':0})
                        l.append({'username':u2,'event':j['event'],'avg':j['best'],'win':0})

                    elif(i['best'] == 0 and j['best'] > 0):
                        l.append({'username':u1,'event':i['event'],'avg':'--','win':0})
                        l.append({'username':u2,'event':j['event'],'avg':j['best'],'win':1})

                    elif(i['best'] > 0 and j['best'] == 0):
                        l.append({'username':u1,'event':i['event'],'avg':i['best'],'win':1})
                        l.append({'username':u2,'event':j['event'],'avg':'--','win':0})

        for i in r1['best']:
            flag = 0
            for j in r2['best']:
                if(i['event'] == j['event']):
                    flag = 1
            if(flag == 0):
                if(i['best'] != 0):
                    l.append({'username':u1,'event':i['event'],'avg':i['best'],'win':1})
                    l.append({'username':u2,'event':i['event'],'avg':'--','win':0})

        for i in r2['best']:
            flag = 0
            for j in r1['best']:
                if(i['event'] == j['event']):
                    flag = 1
            if(flag == 0):
                if(i['best'] != 0):
                    l.append({'username':u1,'event':i['event'],'avg':'--','win':0})
                    l.append({'username':u2,'event':i['event'],'avg':i['best'],'win':1})

    return l

#pk的展示函数, u1:选手1, u2:选手2
def pk_display(u1:str,u2:str):
    pk_list = pklist(u1,u2)
    if(pk_list == -4):
        msg = "输入选手名有误~"
        return msg
    elif(pk_list == -3):
        msg = f"{u1}暂无SCUCA官方成绩~"
        return msg
    elif(pk_list == -2):
        msg = f"{u2}暂无SCUCA官方成绩~"
        return msg
    elif(pk_list == -1):
        msg = f"{u1}和{u2}暂无SCUCA官方成绩~"
        return msg
    elif(pk_list == 0):
        msg = "别在这理发店😠"
        return msg
    else:
        pk_list.sort(key=lambda x:CubeEvent.index(x['event']))
        msg = [
              [u1,'VS',u2]
              ]
        score1 = 0
        score2 = 0
        for r in range(0,len(pk_list),2):
            i = pk_list[r]
            j = pk_list[r+1]
            if(i['win'] == 1 and j['win'] == 0):
                if(j['avg'] == '--'):
                    msg.append([f"{time_convert(i['avg'])}(赢！)",  i['event'], j['avg']])
                else:
                    msg.append([f"{time_convert(i['avg'])}(赢！)",  i['event'], time_convert(j['avg'])])
                score1 += 1
            elif(i['win'] == 0 and j['win'] == 1):
                if(i['avg'] == '--'):
                    msg.append([i['avg'],  i['event'], f"{time_convert(j['avg'])}(赢！)"])
                else:
                    msg.append([time_convert(i['avg']),  i['event'], f"{time_convert(j['avg'])}(赢！)"])
                score2 += 1
            else:
                msg.append([time_convert(i['avg']),  i['event'], time_convert(j['avg'])])
       
        if(score1 > score2):
            if score1 - score2 < 3:
                msg.append([f"(小赢！){u1}",f"{score1} : {score2}",u2])
            elif score1 - score2 < 6:
                msg.append([f"(中赢！){u1}",f"{score1} : {score2}",u2])
            elif score1 - score2 < 9:
                msg.append([f"(大赢！){u1}",f"{score1} : {score2}",u2])
            else:
                msg.append([f"(赢麻！){u1}",f"{score1} : {score2}",u2])
        elif(score1 < score2):
            if score2 - score1 < 3:
                msg.append([u1,f"{score1} : {score2}",f"(小赢！){u2}"])
            elif score2 - score1 < 6:
                msg.append([u1,f"{score1} : {score2}",f"(中赢！){u2}"])
            elif score2 - score1 < 9:
                msg.append([u1,f"{score1} : {score2}",f"(大赢！){u2}"])
            else:
                msg.append([u1,f"{score1} : {score2}",f"(赢麻！){u2}"])
        else:
            msg.append([u1,f"{score1} : {score2}双赢！",u2])

        row = len(msg)
        img = create_table(800, 80*row, _font_path, 30, row, 3, msg, [], [0,1,2])
        img.save('pk.png')
        img = MessageSegment.image('file:///' + os.path.abspath('pk.png'))

        return img

