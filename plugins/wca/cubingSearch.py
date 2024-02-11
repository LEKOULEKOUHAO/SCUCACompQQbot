import requests
import bs4

# 搜索请求标头
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

def fetchSearchResult(nameOrId: str) -> list[tuple[str, str]]:
    """
    获取关键词搜索选手得到的搜索结果
    :param nameOrId: str
    :return: list[tuple[str, str]] 列表中每个元素是元组 (姓名, WCA ID)

    返回示例
    [
        ('Ailun Li (李艾伦)', '2018LIAI01'),
        ('An Li (李安)', '2018LIAN23')
    ]
    """

    url = f'https://cubing.com/results/person?region=World&gender=all&name={nameOrId}'
    res = requests.get(url, headers=headers)

    # table.table-bordered.table-condensed.table-hover.table-boxed的tbody下的诸tr
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', class_='table-bordered')

    tbody = table.find('tbody')
    trs = tbody.find_all('tr')[:10]

    # 若未找到数据，返回空列表
    if len(trs) == 1 and trs[0].find_all('td')[0].find('span').text == '没有找到数据.':
        return []

    # 每个tr下有5个td，分别是：较量按钮、姓名、WCA ID、地区、性别，我们只需要姓名和WCA ID
    namesAndIds = [(tr.find_all('td')[1].text, tr.find_all('td')[2].text) for tr in trs]

    return namesAndIds

