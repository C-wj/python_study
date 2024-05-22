import httpx

base_url = 'https://crm.10039.cc'
url = "/crm/uploadImgController/upload"

headers = {
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://crm.10039.cc/crm/dialog/showCreateCustDialog?isfalg=2',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Host': 'crm.10039.cc',
    'Cookie': 'SESSION=ada43e6f-4200-48cd-b143-67d288ef8b8f; login_sms_zhangwenrui=1; 274f48c7d0ac42f7bb300f6b6f05cfb9=WyIzNDE2NDM5NjQ4Il0'
}

with httpx.Client(base_url=base_url) as client:
    faceUResult = client.get('https://oss-education.oss-accelerate.aliyuncs.com/1564153514236964866.jpg')

    files = {'uploadFile': ('正面.jpg', faceUResult.read(), 'image/jpeg')}
    param = {'dir': 'image'}
    payload = {'type': 0,
               'fileId': '',
               'localUrl': f'C:\\fakepath\\正面.jpg'}
    response = client.request("POST", url, headers=headers, data=payload, params=param, files=files)
    print(response.text)
