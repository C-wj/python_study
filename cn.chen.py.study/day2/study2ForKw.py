import requests

# 爬取搜狗首页的页面数据
if __name__ == '__main__':
    url = 'https://www.sogou.com/web'

    kw = input("请输入需要查询的内容：")

    param = {
        'query': kw
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    response = requests.get(url=url, headers=headers, params=param, verify=False, timeout=4)
    page_text = response.text
    print(page_text)
    with open('./baidu.html', 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print('爬取陈工')
