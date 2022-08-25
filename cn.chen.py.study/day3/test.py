from time import sleep

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}
base_cookie = 'login_sms_zhangwenrui=1;95fa6890880a433a8094107a65abbb23=WyIzNDE2NDM5NjQ4Il0'

home_url = 'https://crm.10039.cc/crm/manager/login/login.jsp'
yzm_url = 'https://crm.10039.cc/crm/validateCode'
login_url = 'https://crm.10039.cc/crm/loginController/login'

s = requests.session()
headers['Cookies'] = base_cookie
loginResult = s.get(home_url, headers=headers)
SESSION = loginResult.cookies['SESSION']
print(SESSION)
cookie = 'SESSION=' + SESSION + ";" + base_cookie
headers['Cookies'] = cookie
yzmResult = s.get(yzm_url, headers=headers)
print(yzmResult.content)
sleep(1)
with open("./yzm.png", "wb") as f:
    f.write(yzmResult.content)

yzm = input("请输入你看到的验证码")
headers['Content-Type'] = 'application/x-www-form-urlencoded'
data = {'staffCode': 'zhangwenrui', 'password': 'Abc1234', 'validatecode': yzm}
loginR = s.post(login_url, headers=headers, data=data, allow_redirects=False)
print(loginR.cookies)
print(loginR)
s.close()
