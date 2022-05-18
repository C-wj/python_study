import random
import time
from bs4 import BeautifulSoup
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return web_data


def get_random_ip(ip_list):
    proxy_ip = random.choice(str(ip_list))
    proxies = {proxy_ip}
    return proxies


if __name__ == '__main__':

    url = 'https://www.so.com/s'

    mobileList = [
        "16517175614"]

    url_ip = 'http://121.4.186.148:5555/get'
    ip_list = get_ip_list(url_ip, headers)

    for mobile in mobileList:
        proxies = get_random_ip(ip_list)
        param = {
            'q': mobile,
            'src': 'srp',
            # 'ssid': 'b2a75f210b0a4785bd370a782be95901',
            'fr': 'none',
            'psid': 'd80012094281c63cf2b8873604ccd123'
            # "nlpv": "test_bt_15"
        }
        sleepTime = random.randint(15, 30)
        print("睡眠开始" + str(sleepTime))
        time.sleep(sleepTime)
        print("睡眠结束")
        response = requests.get(url=url, params=param, headers=headers, proxies=proxies, timeout=4)
        page_text = response.text
        with open('./369.html', 'w', encoding='utf-8') as fp:
            fp.write(page_text)
        tree = etree.HTML(page_text)
        error_title = tree.xpath("//head/title/text()")
        if error_title:
            title = tree.xpath("//head/title/text()")[0]
            if "访问异常页面" == title:
                print(mobile + "访问异常页面")
                break
        markContent = tree.xpath("//div[@class='mohe-tips']/span[1]/text()")
        markContent1 = tree.xpath("//div[@class='mohe-tips']/span[2]//text()")
        print(mobile + '查询成功')
        if markContent == []:
            print(mobile + '未标记')
            continue
        with open('programming1.txt', 'a', encoding='utf-8') as fp:
            fp.write(mobile + '\n' + str(markContent) + '\n' + str(markContent1) + '\n')
            print(mobile + '写入成功')

print('爬取完成')
