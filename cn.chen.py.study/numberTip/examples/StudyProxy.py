from wsgiref import headers

import requests
from w3lib.http import basic_auth_header

if __name__ == '__main__':
    res = requests.get(
        'http://13113683386.user.xiecaiyun.com/api/proxies?action=getText&key=NPF3452976&count=1&word=&rand=true&norepeat=false&detail=false&ltime=0')
    proxy = f'http://{res.text}'.replace('\n', '')
    print("代理账户"+proxy)

    headers['Proxy-Authorization'] = basic_auth_header('13113683386', '13113683386')

