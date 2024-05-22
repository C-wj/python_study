import asyncio
from time import sleep

import httpx

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
base_cookie = 'login_sms_zhangwenrui=1;95fa6890880a433a8094107a65abbb23=WyIzNDE2NDM5NjQ4Il0'

login_headers = {}

home_url = 'https://crm.10039.cc/crm/manager/login/login.jsp'
yzm_url = 'https://crm.10039.cc/crm/validateCode'
login_url = 'https://crm.10039.cc/crm/loginController/login'
upload_url = 'https://crm.10039.cc/crm/uploadImgController/upload'
getRoutDeparts_url = '/crm/loginController/getRoutDeparts'

class Crm:
    def __int__(self):
        self.base_url = 'https://crm.10039.cc'
        self.headers = {
            'Host': 'crm.10039.cc',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        self.client = self.getClient()
        self.base_cookie = 'login_sms_zhangwenrui=1;95fa6890880a433a8094107a65abbb23=WyIzNDE2NDM5NjQ4Il0'

    def getClient(self):
        client = httpx.Client(base_url=self.base_url, headers=self.headers)
        return client

    def getRout(self, data):
        # 获取渠道
        routDeparts = self.client.post(getRoutDeparts_url, data=data, headers=self.headers)
        return routDeparts.json()

    def setCookie(self, cookie):
        self.headers.update(cookie)


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
    c = Crm()
    asyncio.run(c.run())

    # 获取登录cookie
    # login_cookie = getLoginCookie()
    # login_cookie = 'SESSION=' + '6e827b66-1b1d-42c9-a109-17408b7b0d94' + ";" + base_cookie
    #
    # headers['Cookies'] = login_cookie

    # headers[
    #     'Authorization'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwiYXVkIjoiYWRtaW4iLCJpc3MiOiJlYXN5NGouc2VjdXJpdHkiLCJleHAiOjE2NjE1MDIyNjUsImlhdCI6MTY2MTQ4MDY2NX0.3FkXvFp1rA8M9hxY8tm8ZfL_ePaKRkNWD7YlZUtnES0'

    # login_headers = headers
    # login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # print(login_headers)

    # 上传图片
    with httpx.Client(verify=False) as client:
        param = {'dir', 'image'}
    imagePath = './正面.jpg'

    files = {'uploadFile': ('正面.jpg', open(imagePath, 'rb'), 'image/jpeg')}
    uploadR = client.post(login_url, headers=login_headers, files=files, params=param)
    # uploadR = client.post("http://192.168.6.56/voice-manage/sys_files", files=files, headers=headers)
    print(uploadR.text)
    # login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # data = {"departNameFilter": "深圳", "sort": "province_code", "order": "asc"}
    # routR = client.post("https://crm.10039.cc/crm/loginController/getRoutDeparts", data=data, headers=login_headers,
    #                     follow_redirects=False)
    # print(routR)
    # print(routR.json())
