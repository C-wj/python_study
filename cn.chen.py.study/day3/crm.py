from time import sleep

import httpx

headers = {
    'Host': 'crm.10039.cc',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
base_cookie = 'login_sms_zhangwenrui=1;95fa6890880a433a8094107a65abbb23=WyIzNDE2NDM5NjQ4Il0'

login_headers = {}

home_url = 'https://crm.10039.cc/crm/manager/login/login.jsp'
yzm_url = 'https://crm.10039.cc/crm/validateCode'
login_url = 'https://crm.10039.cc/crm/loginController/login'
upload_url = 'https://crm.10039.cc/crm/uploadImgController/upload'
fiddler_proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def getLoginCookie():
    with httpx.Client() as s:
        headers['Cookies'] = base_cookie
        loginResult = s.get(home_url, headers=headers)
        SESSION = loginResult.cookies['SESSION']

        print(SESSION)

        cookie = 'SESSION=' + SESSION + ";" + base_cookie

        headers['Cookies'] = cookie
        yzmResult = s.get(yzm_url, headers=headers)
        print(yzmResult.content)
        sleep(1)
        with open("./yzm.png", 'wb') as f:
            f.write(yzmResult.content)

        yzm = input("请输入你看到的验证码")

        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        data = {'staffCode': 'zhangwenrui', 'password': 'Abc1234', 'validatecode': yzm}
        loginR = s.post(login_url, headers=headers, data=data, follow_redirects=False)
        login_session = loginR.cookies['SESSION']
        print("login_session:" + login_session)
        return 'SESSION=' + login_session + ";" + base_cookie


if __name__ == '__main__':
    # 获取登录cookie
    # login_cookie = getLoginCookie()
    login_cookie = 'SESSION=' + '54ec2cd0-144d-4253-8976-fc28ce318073' + ";" + base_cookie

    headers['Cookie'] = login_cookie

    login_headers = headers
    print(login_headers)

    # 上传图片
    with httpx.Client() as client:
        imagePath = './正面.jpg'

        files = {'uploadFile': ('正面.jpg', open(imagePath, 'rb'), 'image/jpeg')}
        uploadR = client.post(upload_url + '?dir=image', headers=login_headers, files=files)
        print(uploadR)
        print(uploadR.text)
        # login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
        # data = {"departNameFilter": "深圳", "sort": "province_code", "order": "asc"}
        # routR = client.post("https://crm.10039.cc/crm/loginController/getRoutDeparts", data=data, headers=login_headers,
        #                     follow_redirects=False)
        # print(routR)
        # print(routR.json())
