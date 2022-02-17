from bs4 import BeautifulSoup
import requests

from confing import *

def getProxyList(target_url=TARGET_URL, n=4):
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}

    html = requests.get(target_url, headers=header)
    
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='ip_list').find_all('tr')
    for tr in trs[1:]:
        tds = tr.find_all('td')
        # 国家
        if tds[1].find('img') is None:
            nation = '未知'
            locate = '未知'
        else:
            nation = tds[1].find('img')['alt'].strip()
            locate = tds[4].text.strip()
            
        ip = tds[1].text.strip()
        port = tds[2].text.strip()
        anony = tds[5].text.strip()
        protocol = tds[6].text.strip()
        speed = tds[7].find('div')['title'].strip()
        time = tds[9].text.strip()
        print('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol, speed, time))
        yield ':'.join([ip,port])
