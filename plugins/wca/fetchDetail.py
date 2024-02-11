import requests
import bs4

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

def fetchDetail(wcaId: str) -> dict[str, str or dict[str, dict]]:
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

