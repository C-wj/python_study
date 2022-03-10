import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

if __name__ == '__main__':
    # kw = input('请输入要查询的手机号码')

    param = {
        'q': '19937800100'
    }

    sogou = 'http://s1.cscmjc.com/api/wap/sogouwap.php'

    url_360 = 'http://s1.cscmjc.com/api/wap/souswap360.php'

    response = requests.get(url=sogou, params=param, headers=headers)
    page_text = response.text
    tree = etree.HTML(page_text)
    markPlatform = tree.xpath("//tr/td[1]/text()")
    markStatus = tree.xpath("//tr/td[2]/text()")
    print(markPlatform)
