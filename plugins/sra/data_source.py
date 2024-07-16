sra_url = 'https://ss.sxmfxh.com/' # 基url

#sra_url = 'https://ss.sxmfxh.com:5000/' # 测试服，使用时注释掉

comp_url = sra_url + 'comps/getCompByStatus?query={"c_status":"5,6,7,8","page":1,"size":3}' # 常规赛事

comp_online_url = sra_url + 'comps/getCompByStatusForOnLine?query={"c_status":"5,6,7,8","page":1,"size":3}' # 线上赛事

comp_college_url = sra_url + 'comps/getCompByStatusForCollege?query={"c_status":"5,6,7,8","page":1,"size":3}' # 校园赛事

record_url = sra_url + 'record/getRecordAll' # 历史纪录

#排名，传参：项目id, 排名类型:1为单次，2为平均
def rank_url(e_id:int, type:int):
    #return sra_url + f'rank/getRank?query={"e_id":{str(e_id)},"address":"","page":1,"size":10,"type":{str(type)}}'
    return sra_url + 'rank/getRank?query={"e_id":' + str(e_id) + ',"address":"","page":1,"size":10,"type":' + str(type) + '}'

#成绩，传参：选手id
def grade_url(u_id:int):
    return sra_url + 'grades/getGradesAndRank?query={"u_id":' + str(u_id) + '}'

#选手，传参：选手名或选手id
def user_url(searchInput):
    return sra_url + 'users/getUsers?query={"searchInput":"' + str(searchInput) + '","page":1,"size":10}'

#参赛狂魔，传参：1：所有，2：线下，3：线上
def getCompMost_url(value:int):
    return sra_url + 'fun/getCompMost?query={"value":' + str(value) + '}'

#PB达人，传参：0：所有，其余为项目id
def getPBMost_url(e_id:int):
    return sra_url + 'fun/getPBMost?query={"value":' + str(e_id) + '}'

#无冕之王，传参：项目id
def getNoPodium_url(e_id:int):
    return sra_url + 'fun/getNoPodium?query={"value":' + str(e_id) + '}'

#奖牌遗珠，传参：0：所有，其余为项目id
def getNo4_url(e_id:int):
    return sra_url + 'fun/getNo4?query={"value":' + str(e_id) + '}'

CubeEvent = {
    '333','222','444','555','666','777',
    '333oh','pyram','skewb','minx','333bf','444bf','555bf',
    '333mbf','sq1','333fm','clock','e-333','e-333oh'
}
