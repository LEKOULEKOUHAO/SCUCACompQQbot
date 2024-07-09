import requests
import bs4

from .types import userDetailType

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://cubing.com/results/person',
    'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}


def fetchUserDetail(wcaId: str) -> userDetailType:
    """
    获取wcaId对应的选手详细信息
    :param wcaId: str
    :return: userDetailType

    返回示例
    {
        '姓名': 'Allen Zhang (张西)',
        '地区': '香港',
        '参赛次数': '1',
        'WCA ID': '2019ZHAA02',
        '性别': '男',
        '参赛经历': '2019.08.24 - 2019.08.25',
        'personalRecords': {
            '三阶': {
                'single': {
                    'time': '31.45',
                    'nationalRecord': '757',
                    'continentalRecord': '45530',
                    'worldRecord': '135803'
                },
                'average': {
                    'time': '36.85',
                    'worldRecord': '131595',
                    'continentalRecord': '44132',
                    'nationalRecord': '733'
                }
            },
        }
    }
    """

    url = f'https://cubing.com/results/person/{wcaId}'
    res = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # 1. 个人信息: .panel-body > .row下的诸div
    personalInfoHtml = soup.find('div', class_='panel-body').find_all('div', class_='row')[0].find_all('div')
    # div分别是姓名、地区、参赛次数、WCA ID、性别、参赛经历，每个div下有2个span，分别是标题和内容。我们分别取出内容
    personalInfo = {div.find_all('span')[0].text.strip(': '): div.find_all('span')[1].text.strip() for div in personalInfoHtml}

    # 2. 个人成绩: 第一个table.table-bordered的tbody下的诸tr，每一行代表一个项目，每个tr下有多个tr，第一个是项目名，第5个是单次，第6个是平均
    # 第2,3,4个是单次成绩的地区排名、洲排名、世界排名，第7,8,9个是平均成绩的世界排名、洲排名、地区排名
    personalRecordsHtml = soup.find('table', class_='table-bordered').find('tbody').find_all('tr')
    personalRecords = {
        tr.find_all('td')[0].text.strip(): {
            'single': {
                'time': tr.find_all('td')[4].text,
                'nationalRecord': tr.find_all('td')[1].text,
                'continentalRecord': tr.find_all('td')[2].text,
                'worldRecord': tr.find_all('td')[3].text
            },
            'average': {
                'time': tr.find_all('td')[5].text,
                'worldRecord': tr.find_all('td')[6].text,
                'continentalRecord': tr.find_all('td')[7].text,
                'nationalRecord': tr.find_all('td')[8].text
            }
        }
        for tr in personalRecordsHtml
    }

    # 3. 拼接personalInfo和personalRecords
    return {**personalInfo, 'personalRecords': personalRecords}


def fetchWR(includeOld):
    """
    获取当前世界纪录
    :param includeOld:
    :return:

    返回示例
    [
        {
            'event': '三阶',
            'single': [
                {
                    'player': 'Yusheng Du (杜宇生)',
                    'time': '3.47'
                }
            ],
            'average': [
                {
                    'player': 'Yusheng Du (杜宇生)',
                    'time': '5.53'
                }
            ]
        },
        ...
    ]
    """


    url = f'https://cubing.com/results/records?region=World&type=current'
    res = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    table = soup.find('table', class_='table table-bordered table-condensed table-hover table-boxed')
    trs = table.find('tbody').find_all('tr')
    # class为空的tr表示项目名，其后直到下一个项目名的tr都是该项目的世界纪录，按这个规则分组数据
    WRs = []
    current_WR = {}
    for tr in trs:
        if tr.attrs == {}:
            if current_WR:  # 如果current_WR不为空，说明这至少是第二个项目，将上一个项目的数据加入WRs
                WRs.append(current_WR)
            current_WR = {
                'event': tr.find_all('td')[0].text.strip(),
                'single': [],
                'average': []
            }
        else:
            player = tr.find_all('td')[3].text.strip()
            # 如果player中有括号，且括号里是中文字符，只要括号里的名字，否则只要括号外的名字
            if '(' in player:
                player_name_in = player.split('(')[1].split(')')[0]
                player_name_out = player.split('(')[0]
                if '\u4e00' <= player_name_in[0] <= '\u9fff':
                    player = player_name_in
                else:
                    player = player_name_out

            if tr.find_all('td')[1].text:  # 如果第二个td有内容，说明这是单次成绩，否则是平均成绩
                current_WR['single'].append({
                    'player': player,
                    'time': tr.find_all('td')[1].text.strip(),
                })
            else:
                current_WR['average'].append({
                    'player': player,
                    'time': tr.find_all('td')[2].text.strip(),
                })

    if not includeOld:  # 排除掉已不存在的项目：八板，十二板，脚拧
        WRs = [WR for WR in WRs if WR['event'] not in ['八板', '十二板', '脚拧']]

    return WRs