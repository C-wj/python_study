import random

import requests
from lxml import etree

# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.47']


def gethtml(url, param, headers, proxies):
    i = 0
    while i < 3:
        try:
            response = requests.get(url=url, params=param, headers=headers, proxies=proxies, timeout=10)
            return response.text
        except requests.exceptions.RequestException as e:
            print(e)
            i += 1
            # 内网代理 http://192.168.1.3:8082
            res = requests.get(
                'http://13113683386.user.xiecaiyun.com/api/proxies?action=getText&key=NPF3452976&count=1&word=&rand=true&norepeat=false&detail=false&ltime=0')
            proxy = f'http://{res.text}'.replace('\n', '')
            proxies = {
                'http': proxy
            }


if __name__ == '__main__':

    url = 'https://www.so.com/s'

    mobileList = []

    url_ip = 'http://121.4.186.148:5555/get'
    # ip_list = get_ip_list(url_ip, headers)

    i = 0
    for mobile in mobileList:
        res = requests.get(
            'http://13113683386.user.xiecaiyun.com/api/proxies?action=getText&key=NPF3452976&count=1&word=&rand=true&norepeat=false&detail=false&ltime=0')
        proxy = f'http://{res.text}'.replace('\n', '').replace('\r', '')
        proxies = {
            'http': proxy
        }
        headers = {
            'User-Agent': random.choice(agents),
            'X-Requested-With': 'XMLHttpRequest'
        }
        param = {
            'q': mobile,
            'src': 'srp',
            # 'ssid': 'b2a75f210b0a4785bd370a782be95901',
            'fr': 'none',
            'psid': '32e43664e937f38eb9f1cf8f037a62a7'
            # "nlpv": "test_bt_15"
        }
        page_text = gethtml(url, param, headers, proxies)
        with open('./369.html', 'w', encoding='utf-8') as fp:
            fp.write(page_text)
        tree = etree.HTML(page_text)
        i += 1
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
