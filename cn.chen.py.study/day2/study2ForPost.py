import json

import requests

# 爬取搜狗首页的页面数据
if __name__ == '__main__':
    url = 'https://fanyi.baidu.com/sug'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    kw = input("请输入需要查询的内容：")

    data = {
        'kw': kw
    }

    response = requests.post(url=url, data=data, headers=headers, timeout=4)
    page_text = response.json()
    filename = kw + '.json'
    fp = open('./' + filename, 'w', encoding='utf-8')
    json.dump(page_text, fp, ensure_ascii=False)

    print('爬取陈工')
