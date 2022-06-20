import requests


def getInnerProxy():
    proxy = {'http': 'http://192.168.1.3:8082',
             'https': 'http://192.168.1.3:8082'}
    # page_txt = requests.get(url="https://www.ip138.com/", proxies=proxy, verify=False).text

    page_txt = requests.get(url="https://myip.ipip.net/", proxies={'http': 'http://192.168.1.3:8082', 'https': 'http://192.168.1.3:8082'}, verify=False).text
    print(page_txt)

    return proxy


if __name__ == '__main__':
    getInnerProxy()
