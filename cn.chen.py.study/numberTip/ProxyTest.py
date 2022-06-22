import requests


def getHttpProxy():
    proxies = {
        'http': 'http://192.168.1.3:8082'
    }
    url = 'http://myip.ipip.net/'
    page_text = requests.get(url=url, proxies=proxies).text

    print(page_text)

    return
