# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import csv
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

firmlinks = []
with open('qianhai_house_urls.csv', 'rb') as rawfile:
    filereader = csv.reader(rawfile)
    for url in rawfile:
        raw = url.strip()
        firmlinks.append(raw)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Cookie': 'city=sz; city=sz; sf_source=; s=; indexAdvLunbo=; global_cookie=evhfowekxxt1h1fteddygkm2j13iw38nonj; __utmt_t0=1; __utmt_t1=1; __utmt_t2=1; Rent_StatLog=592e8876-20ba-43c8-85aa-b56ce9e1d765; city=sz; ASP.NET_SessionId=nsbkekjpkqmqzvxral45lvf4; SoufunSessionID_Office=3_1480407941_13407; logGuid=e03e1168-5366-4461-ad18-b1f25eb47623; polling_imei=f77ee828af30f9a9; __utma=147393320.126839503.1480407929.1480407929.1480407929.1; __utmb=147393320.54.10.1480407929; __utmc=147393320; __utmz=147393320.1480407929.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; unique_cookie=U_evhfowekxxt1h1fteddygkm2j13iw38nonj*18'
}


for url in firmlinks:
    try:
        page = requests.get(url, headers=header, stream=True)
    except:
        continue
    print page.status_code
    time.sleep(2)
    soup = BeautifulSoup(page.text, 'lxml')
    title = soup.find('h1')
    if title == None:
        continue
    print title.text.strip()
    price = soup.find('span', attrs={'style': 'font-size: 16px; color: #f30; font-family: Arial; padding-left: 62px;'})
    price_whole = price.text + '元/平米*月'
    address = soup.find_all('dt')
    edit_address = address[3].text.strip()
    data = [title.text.strip(), price_whole, edit_address.replace('\n', '')]
    with open('qianhai_house_data.csv', 'ab+') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerow(data)

print 'finish'