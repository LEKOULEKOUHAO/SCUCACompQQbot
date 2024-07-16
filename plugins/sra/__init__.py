from .data_source import CubeEvent, sra_url, comp_url, comp_college_url, comp_online_url, record_url, grade_url, user_url,rank_url
from .data_source import getCompMost_url, getPBMost_url, getNoPodium_url, getNo4_url
from .utils import response, time_convert, e_id2event, event2e_id, rank_title
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, GroupIncreaseNoticeEvent, Bot, GROUP, Message,MessageSegment

onehelp = on_command("onehelp", aliases={"one帮助"}, permission= GROUP, priority=1)
@onehelp.handle()
async def _(event: GroupMessageEvent):
    msg = 'OneBot指令使用帮助:'
    msg += '\n/one网站   查看One魔方赛事网官网'
    msg += '\n/近期赛事    查看近期常规赛事'
    msg += '\n/线上赛事    查看近期线上赛事'
    msg += '\n/校园赛事    查看近期校园赛事'
    msg += '\n/one  [选手名或选手id]    查询某一选手的One官方成绩'
    msg += '\n/one纪录    查看One历史纪录'
    msg += '\n/one排名  [项目名]    查看某一项目One官方前十'
    msg += '\n/pkone  [选手名或选手id]  [选手名或选手id]    对比两位选手的One官方成绩'
    msg += '\n/参赛狂魔  [所有|线下|线上]    查看参赛次数Top10'
    msg += '\n/PB达人  [项目名]    查看某一项目PB达人Top10'
    msg += '\n/无冕之王  [项目名]    查看某一项目无冕之王Top10'
    msg += '\n/奖牌遗珠  [项目名]    查看某一项目奖牌遗珠Top10'
    await onehelp.finish(msg)

oneweb = on_command("oneweb", aliases={"one网站","one赛事网"}, permission= GROUP, priority=1)
@oneweb.handle()
async def _(event: GroupMessageEvent):
    msg = sra_url
    await oneweb.finish(msg)

applet = on_command("applet", aliases={"小程序"}, permission= GROUP, priority=1)
@applet.handle()
async def _(event: GroupMessageEvent):
    #发送图片 小程序.jpg
    image_path = 'figures/小程序.jpg'
    # 读取图片文件
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    # 构造消息段
    image = MessageSegment.image(image_bytes)
    # 发送图片
    await applet.finish(image)

comp = on_command("comp", aliases={"近期赛事"}, permission= GROUP, priority=1)
@comp.handle()
async def _(event: GroupMessageEvent):
    msg = SRABot.comp(event,comp_url)
    if not msg.strip():
        msg = "获取赛事信息失败"
    await comp.finish(msg)

comp_online = on_command("comp_online", aliases={"线上赛事"}, permission= GROUP, priority=1)
@comp_online.handle()
async def _(event: GroupMessageEvent):
    msg = SRABot.comp(event,comp_online_url)
    await comp_online.finish(msg)

comp_college = on_command("comp_college", aliases={"校园赛事"}, permission= GROUP, priority=1)
@comp_college.handle()
async def _(event: GroupMessageEvent):
    msg = SRABot.comp(event,comp_college_url)
    await comp_college.finish(msg)

sra = on_command("sra", aliases={"官方成绩","one","One","SRA","ONE"}, permission= GROUP, priority=1)
@sra.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await sra.finish("还没输入选手名或选手uid~(使用示例:/one 张三)")

    msg = SRABot.sra(event,args[0])
    await sra.finish(msg)

onerecord = on_command("onerecord", aliases={"one纪录"}, permission= GROUP, priority=1)
@onerecord.handle()
async def _(event: GroupMessageEvent):
    msg = SRABot.record(event)
    await onerecord.finish(msg)

onerank = on_command("onerank", aliases={"one排名"}, permission= GROUP, priority=1)
@onerank.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await onerank.finish("还没输入项目名~(使用示例:/rank 333)")
    elif str(args[0]) not in CubeEvent:
        await onerank.finish("只支持以下项目的排名查询:333, 222, 444, 555, 666, 777, 333oh, pyram, skewb, minx, 333bf, 444bf, 555bf, 333mbf, sq1, 333fm, clock, e-333, e-333oh")
    
    msg = SRABot.rank(event,args[0])
    await onerank.finish(msg)

pkone = on_command("pkone", aliases={"较量one"}, permission= GROUP, priority=1)
@pkone.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await pkone.finish("还没输入选手名~(使用示例:/pk 张三 李四)")
    elif len(args) == 1:
        await pkone.finish("还没输入另一个选手名~(使用示例:/pk 张三 李四)")
    elif len(args) > 2:
        await pkone.finish("输入选手名过多~(使用示例:/pk 张三 李四)")
    
    msg = SRABot.pk(event,args[0],args[1])
    await pkone.finish(msg)

compmost = on_command("compmost", aliases={"参赛狂魔"}, permission= GROUP, priority=1)
@compmost.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await compmost.finish("还没输入选项~(使用示例:/参赛狂魔 所有)")
    elif len(args) > 1:
        await compmost.finish("输入选项过多~(使用示例:/参赛狂魔 所有)")
    elif args[0] not in ['所有','线下','线上']:
        await compmost.finish("只支持以下选项的查询:所有, 线下, 线上")
    
    msg = SRABot.compmost(event,args[0])
    await compmost.finish(msg)

pbmost = on_command("pbmost", aliases={"PB达人","pb达人"}, permission= GROUP, priority=1)
@pbmost.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        msg = SRABot.pbmost(event,None)
        await pbmost.finish(msg)
    elif len(args) > 1:
        await pbmost.finish("输入选项过多~(使用示例:/pb达人 333)")
    elif args[0] not in CubeEvent:
        await pbmost.finish("直接使用命令 /pb达人 为所有项目统计,单个项目只支持以下选项的查询:333, 222, 444, 555, 666, 777, 333oh, pyram, skewb, minx, 333bf, 444bf, 555bf, 333mbf, sq1, 333fm, clock, e-333, e-333oh")
    
    msg = SRABot.pbmost(event,args[0])
    await pbmost.finish(msg)

getnopodium = on_command("getnopodium", aliases={"无冕之王"}, permission= GROUP, priority=1)
@getnopodium.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        await getnopodium.finish("还没输入项目名~(使用示例:/无冕之王 333)")
    elif len(args) > 1:
        await getnopodium.finish("输入项目名过多~(使用示例:/无冕之王 333)")
    elif args[0] not in CubeEvent:
        await getnopodium.finish("只支持以下项目的查询:333, 222, 444, 555, 666, 777, 333oh, pyram, skewb, minx, 333bf, 444bf, 555bf, 333mbf, sq1, 333fm, clock, e-333, e-333oh")
    
    msg = SRABot.getnopodium(event,args[0])
    await getnopodium.finish(msg)

getno4 = on_command("getno4", aliases={"奖牌遗珠"}, permission= GROUP, priority=1)
@getno4.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    args = args.extract_plain_text().strip().split()
    if not args:
        msg = SRABot.getno4(event,None)
        await getno4.finish(msg)
    elif len(args) > 1:
        await getno4.finish("输入项目名过多~(使用示例:/奖牌遗珠 333)")
    elif args[0] not in CubeEvent:
        await getno4.finish("只支持以下项目的查询:333, 222, 444, 555, 666, 777, 333oh, pyram, skewb, minx, 333bf, 444bf, 555bf, 333mbf, sq1, 333fm, clock, e-333, e-333oh")
    
    msg = SRABot.getno4(event,args[0])
    await getno4.finish(msg)

class SRABot:
    def comp(event:MessageEvent, url:str):
        if response(url)['code'] != 10000:
            msg = '赛事信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            if url == comp_url:
                msg = '近期常规赛事如下:'
            elif url == comp_online_url:
                msg = '近期线上赛事如下:'
            elif url == comp_college_url:
                msg = '近期校园赛事如下:'
            
            l = response(url)['data']
            count = 0
            for i in l:
                count += 1
                msg += '\n' + str(count) + '.' + i['c_name']
                msg += '\n' + sra_url + '#/comp?id=' + str(i['c_id'])
            
        return msg
    
    def sra(event:MessageEvent, searchInput):
        if response(user_url(searchInput))['code'] != 10000:
            msg = '选手信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'
        
        else:
            user = response(user_url(searchInput))['data']
            if(len(user) == 0):
                msg = '未查询到该选手,请检查选手名或选手id是否输入正确~'

            elif(len(user) > 1):
                msg = '查询到以下多个选手,请根据选手uid进行查询~'
                for i in user:
                    msg += '\n' + i['u_name'] + '(u_id:' + str(i['u_id']) + ')'

                if len(user) == 10:
                    msg += '\n…………'

            else:
                u_id = user[0]['u_id']
                u_name = user[0]['u_name']
                url = grade_url(u_id)
                l = response(url)['data']['rank']
                if(l):
                    msg = u_name + '(u_id:' + str(u_id) + ')' + '的One官方成绩如下:'
                    #过滤出l中e_id为1到17或者41、42的元素
                    l = list(filter(lambda x: x['e_id'] in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,41,42], l))
                    msg += '\n项目    单次    ||    平均'
                    for i in l:
                        msg += '\n' + e_id2event(i['e_id']) + '    ' + time_convert(i['time_single']) + '  ' + '  ||  '  + '  ' + time_convert(i['time_avg'])

                else:
                    msg = u_name + '(u_id:' + str(u_id) + ')' + '暂无官方成绩~'

        return msg
    
    def record(event:MessageEvent):
        if response(record_url)['code'] != 10000:
            msg = '纪录获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            msg = 'One纪录如下:'
            msg += '\n项目    单次    ||    平均'
            l = response(record_url)['data']
            for i in l:
                msg += '\n' + e_id2event(i['e_id']) + '   '
                msg += i['s']['u_name'] + '   ' + time_convert(i['s']['t_single']) + '  ||  '
                msg += i['a']['u_name'] + '   ' + time_convert(i['a']['t_avg'])
        
        return msg
    
    def rank(event:MessageEvent, eventInput):
        if response(rank_url(event2e_id(eventInput),1))['code'] != 10000 and response(rank_url(event2e_id(eventInput),2))['code'] != 10000:
            msg = '排名信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            l_s = response(rank_url(event2e_id(eventInput),1))['data']
            l_a = response(rank_url(event2e_id(eventInput),2))['data']
            if len(l_s) != 0 or len(l_a) != 0:
                msg = rank_title(eventInput)
                msg += '\n    单次  ||  平均'
                if len(l_s) >= 10:
                    l_s = list(map(lambda x: [x['u_name'], x['time_single']], l_s[0:10]))
                else:
                    l_s = list(map(lambda x: [x['u_name'], x['time_single']], l_s))
                if len(l_a) >= 10:
                    l_a = list(map(lambda x: [x['u_name'], x['time_avg']], l_a[0:10]))
                else:
                    l_a = list(map(lambda x: [x['u_name'], x['time_avg']], l_a))
                for i in range(min(len(l_s), len(l_a), 10)):
                    msg += '\n' + l_s[i][0] + '  ' + time_convert(l_s[i][1]) + '  ||  ' + l_a[i][0] + '  ' + time_convert(l_a[i][1])

            else:
                msg = eventInput + '项目暂无One官方成绩~'

        return msg
    
    def pk(event:MessageEvent, searchInput1, searchInput2):
        if response(user_url(searchInput1))['code'] != 10000 or response(user_url(searchInput2))['code'] != 10000:
            msg = '选手信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            user1 = response(user_url(searchInput1))['data']
            user2 = response(user_url(searchInput2))['data']
            if(len(user1) == 0 or len(user2) == 0):
                msg = '未查询到该选手,请检查选手名或选手id是否输入正确~'

            elif(len(user1) > 1 or len(user2) > 1):
                msg = '查询到以下多个选手,请根据选手uid进行pk~'
                for i in user1:
                    msg += '\n' + i['u_name'] + '(u_id:' + str(i['u_id']) + ')'
                for i in user2:
                    msg += '\n' + i['u_name'] + '(u_id:' + str(i['u_id']) + ')'

                if len(user1) == 10 or len(user2) == 10:
                    msg += '\n…………'

            else:
                u_id1 = user1[0]['u_id']
                u_name1 = user1[0]['u_name']
                u_id2 = user2[0]['u_id']
                u_name2 = user2[0]['u_name']
                url1 = grade_url(u_id1)
                url2 = grade_url(u_id2)
                l1 = response(url1)['data']['rank']
                l2 = response(url2)['data']['rank']
                #过滤出l1和l2中e_id为1到17或者41、42的元素,暂时不考虑多盲(14)
                l1 = list(filter(lambda x: x['e_id'] in [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,41,42], l1))
                l2 = list(filter(lambda x: x['e_id'] in [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17,41,42], l2))
                #过滤出l1和l2中e_id的并集,对项目去重
                l = list(set(map(lambda x: x['e_id'], l1 + l2)))
                #对l中e_id从小到大排序
                l.sort()
                #对于此集中l1缺乏的项目，补充进l1中，time_single和time_avg均为0
                for i in l:
                    if i not in list(map(lambda x: x['e_id'], l1)):
                        l1.append({'e_id':i,'time_single':0,'time_avg':0})
                #对于此集中l2缺乏的项目，补充进l2中，time_single和time_avg均为0
                for i in l:
                    if i not in list(map(lambda x: x['e_id'], l2)):
                        l2.append({'e_id':i,'time_single':0,'time_avg':0})
                
                #对l1和l2中e_id从小到大排序
                l1.sort(key=lambda x: x['e_id'])
                l2.sort(key=lambda x: x['e_id'])   
                msg = u_name1 + '(u_id:' + str(u_id1) + ')' + '与' + u_name2 + '(u_id:' + str(u_id2) + ')' + 'PK结果如下:'
                score1 = 0
                score2 = 0
                for i in range(len(l1)):
                    if l1[i]['e_id'] in [11,12,13]:
                        if l1[i]['time_single'] == 0:
                            if l2[i]['time_single'] != 999999:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + '--' + '  ||  ' + time_convert(l2[i]['time_single']) + '(☆)'
                                score2 += 1
                            else:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + '--' + '  ||  ' + 'DNF' + '    '
                        elif l2[i]['time_single'] == 0:
                            if l1[i]['time_single'] != 999999:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_single']) + '(☆)' + '  ||  ' + '--'
                                score1 += 1
                            else:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + 'DNF' + '  ||  ' + '--'
                        elif l1[i]['time_single'] < l2[i]['time_single']:
                            msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_single']) + '(☆)' + '  ||  ' + time_convert(l2[i]['time_single'])
                            score1 += 1
                        elif l1[i]['time_single'] > l2[i]['time_single']:
                            msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_single']) + '  ||  ' + time_convert(l2[i]['time_single']) + '(☆)'
                            score2 += 1
                        else:
                            msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_single']) + '  ||  ' + time_convert(l2[i]['time_single'])
                    else:
                        if l1[i]['time_avg'] == 0:
                            if l2[i]['time_avg'] != 999999:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + '--' + '  ||  ' + time_convert(l2[i]['time_avg']) + '(☆)'
                                score2 += 1
                            else:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + '--' + '  ||  ' + 'DNF'
                        elif l2[i]['time_avg'] == 0:
                            if l1[i]['time_avg'] != 999999:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_avg']) + '(☆)' + '  ||  ' + '--'
                                score1 += 1
                            else:
                                msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + 'DNF' + '  ||  ' + '--'
                        elif l1[i]['time_avg'] < l2[i]['time_avg']:
                            msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_avg']) + '(☆)' + '  ||  ' + time_convert(l2[i]['time_avg'])
                            score1 += 1
                        elif l1[i]['time_avg'] > l2[i]['time_avg']:
                            msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_avg']) + '  ||  ' + time_convert(l2[i]['time_avg']) + '(☆)'
                            score2 += 1
                        else:
                            msg += '\n' + e_id2event(l1[i]['e_id']) + '    ' + time_convert(l1[i]['time_avg']) + '  ||  ' + time_convert(l2[i]['time_avg'])
                
                if score1 > score2:
                    msg += '\n' + u_name1 + ' ' + str(score1) + '(☆)' + ':' + str(score2) + ' ' + u_name2
                elif score1 < score2:
                    msg += '\n' + u_name1 + ' ' + str(score1) + ':' + str(score2) + '(☆)' + ' ' + u_name2
                else:
                    msg += '\n' + u_name1 + ' ' + str(score1) + ':' + str(score2) + ' ' + u_name2

        return msg
    
    def compmost(event:MessageEvent, value):
        match value:
            case '所有':
                value = 1
            case '线下':
                value = 2
            case '线上':
                value = 3

        if response(getCompMost_url(str(value)))['code'] != 10000:
            msg = '参赛狂魔信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            if value == 1:
                msg = '【参赛狂魔Top10】'
            elif value == 2:
                msg = '【线下参赛狂魔Top10】'
            elif value == 3:
                msg = '【线上参赛狂魔Top10】'
            
            l = response(getCompMost_url(value))['data']
            for i in l:
                msg += '\n' + i['u_name'] + '  参赛次数:  ' + str(i['total'])
        
        return msg
    
    def pbmost(event:MessageEvent, value):
        if response(getPBMost_url(str(event2e_id(str(value)))))['code'] != 10000:
            msg = 'PB达人信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            msg = '【PB达人Top10】'
            if value == None:
                msg += '\n    全项目'
            else:
                msg += '\n    ' + value + '项目'
            
            l = response(getPBMost_url(str(event2e_id(str(value)))))['data']
            if len(l) == 0:
                msg = '该项目暂无数据~'
            else:
                for i in l:
                    msg += '\n' + i['u_name'] + '  PB次数:  ' + '单次:' + str(i['totalS']) + '  平均:' + str(i['totalA'])
                    msg += '  总计:' + str(i['totalS'] + i['totalA'])
        
        return msg
    
    def getnopodium(event:MessageEvent, value):
        if response(getNoPodium_url(str(event2e_id(str(value)))))['code'] != 10000:
            msg = '无冕之王信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            msg = '【无冕之王Top10】'
            msg += '\n统计从未获奖但实力强劲的选手'
            if value == None:
                msg += '   全项目'
            else:
                msg += '\n    ' + value + '项目'
            
            l = response(getNoPodium_url(str(event2e_id(str(value)))))['data']
            if len(l) == 0:
                msg = '该项目暂无数据~'
            else:
                for i in l:
                    msg += '\n' + i['u_name'] + '  单次:' + time_convert(i['time_single']) + '  平均:' + time_convert(i['time_avg'])
        
        return msg
    
    def getno4(event:MessageEvent, value):
        if response(getNo4_url(str(event2e_id(str(value)))))['code'] != 10000:
            msg = '奖牌遗珠信息获取失败,可能是由于One官网正在维护或者接口失效,请稍后再试~'

        else:
            msg = '【奖牌遗珠Top10】'
            msg += '\n统计殿军次数最多的选手'
            if value == None:
                msg += '\n    全项目  '
            else:
                msg += '\n    ' + value + '项目  '
            
            l = response(getNo4_url(str(event2e_id(str(value)))))['data']
            if len(l) == 0:
                msg = '该项目暂无数据~'
            else:
                for i in l:
                    msg += '\n' + i['u_name'] + '   次数:   ' + str(i['total'])
        
        return msg