import time

import requests
import uvicorn
import yaml
from fastapi import FastAPI
from loguru import logger
from playwright.sync_api import Playwright, sync_playwright
from pydantic import BaseModel

yzm_url = 'https://crm.10039.cc/crm/validateCode'
ocr_url = 'http://192.168.1.91:9898/ocr/file'

app = FastAPI()


class PostBody(BaseModel):
    msisdn: str
    city: str
    faceUrl: str
    backUrl: str
    holdUrl: str


@app.post("/create")
def create(postBody: PostBody):
    logger.info(f'postBody:{postBody.json()}')
    c = crm()
    try:
        logger.info(f'postBody:{postBody.json()}')
        runPlayWRight(postBody, c)
    except Exception as e:
        logger.error(f'处理失败{e}')
        return {"success": "false", "msg": c.msg + e}
    return {"success": "true"}


class crm:
    def __init__(self):
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
        }
        self.cookie = ['login_sms_zhangwenrui=1']
        self.queryResult = None
        self.msg = None

    @classmethod
    def on_response(cls, response, url):
        if '/VCommonController/qryAllUserInfo' in response.url and response.status == 200:
            print("%s得到的响应为：" % url, response.json())
            qryAllUserInfoResult = response.json()
            # global queryResult
            cls.queryResult = qryAllUserInfoResult.get("success")
            # global msg
            cls.msg = qryAllUserInfoResult.get("msg")


def run(playwright: Playwright, postBody=None, c=None) -> None:
    browser = playwright.chromium.launch(headless=False, channel='chrome', slow_mo=500)
    context = browser.new_context()
    context.add_cookies(
        cookies=[{'name': 'login_sms_zhangwenrui', 'value': '1', 'path': '/', 'domain': 'crm.10039.cc'}])

    # Open new page
    page = context.new_page()

    url = "https://crm.10039.cc/crm/manager/login/login.jsp"
    # Go to https://crm.10039.cc/crm/manager/login/login.jsp
    page.goto(url)

    cookies = context.cookies()
    cookiesFor = ''
    for cookie in cookies:
        cookiesFor += cookie.get('name') + '=' + cookie.get('value') + ';'
    print(cookiesFor)

    c.headers['Cookie'] = cookiesFor
    yzmResult = requests.get(yzm_url, headers=c.headers)
    print(yzmResult.content)
    yzmFile = {'image': yzmResult.content}
    res = requests.post(ocr_url, files=yzmFile, timeout=4)

    # Fill [placeholder="请输入工号"]
    page.locator("[placeholder=\"请输入工号\"]").fill(username)

    # Fill [placeholder="请输入密码"]
    page.locator("[placeholder=\"请输入密码\"]").fill(password)

    # Fill [placeholder="验证码"]
    page.locator("[placeholder=\"验证码\"]").fill(res.text)

    # Click input:has-text("登录")
    page.locator("input:has-text(\"登录\")").click()
    page.wait_for_url("https://crm.10039.cc/crm/layout/home.jsp")

    # Click text=营业受理
    page.locator("text=营业受理").click()

    # Click text=批量开户
    page.locator("text=批量开户").click()

    # Click text=客户资料返档
    page.locator("text=客户资料返档").click()
    page.wait_for_url("https://crm.10039.cc/crm/costomerDataReverseController/costomerDataReverseInit?tradeTypeCode=90")

    # Click [id="s"]
    page.locator("[id=\"s\"]").click()

    # Click [placeholder="渠道名称"]
    page.locator("[placeholder=\"渠道名称\"]").click()

    # Fill [placeholder="渠道名称"]
    page.locator("[placeholder=\"渠道名称\"]").fill(postBody.city)

    # Click text=  <input type="button" id="" onclick="onclic()" value="查询" class="form_sub_2">
    page.click("//input[@onclick=\"onclic()\"]")

    # Click .datagrid-view2 > .datagrid-body
    print('查询点击1')
    page.click('.datagrid-view2 > .datagrid-body')
    print('查询点击2')
    # Click span:has-text("确定") >> nth=0

    # Click a:has-text("确定")
    page.click("//span[text()=\"确定\"][@class=\"l-btn-text\"]")

    # Click input[name="identityNum"]
    page.locator("input[name=\"identityNum\"]").click()

    # Fill input[name="identityNum"]
    page.locator("input[name=\"identityNum\"]").fill(postBody.msisdn)

    # Click input[name="button"]
    page.locator("input[name=\"button\"]").click()

    # Click text=下一步
    page.locator("text=下一步").click()
    page.wait_for_url(
        "https://crm.10039.cc/crm/costomerDataReverseController/costomerDataReverseRedirect?serialNumber=" + postBody.msisdn + "&packageKindCode=X001LXTC&tradeTypeCode=90")

    page.on('response',
            lambda response: crm.on_response(response, "https://crm.10039.cc/crm/VCommonController/qryAllUserInfo"))
    assert c.queryResult == 'success'
    time.sleep(2)

    # Click text=新建客户
    page.locator("text=新建客户").click()
    logger.info('新建客户')
    # Click input[name="custPhoto"] >> nth=0
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"custPhoto\"]").first.click()
    faceUrl = postBody.faceUrl
    faceUResult = requests.get(faceUrl)
    faceFiles = [{"name": "正面.jpg", "mimeType": "image/jpeg", "buffer": faceUResult.content}]
    # Upload 1a8cd62204730ce7399f8e51ff01eb0.jpg
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"uploadFile\"]").set_input_files(
        files=faceFiles)

    # Click text=确定
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("text=确定").click()
    time.sleep(2)
    # Click input[name="custPhoto"] >> nth=1
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"custPhoto\"]").nth(1).click()

    backUrl = postBody.backUrl
    backResult = requests.get(backUrl)
    backFiles = [{"name": "背面.jpg", "mimeType": "image/jpeg", "buffer": backResult.content}]

    # Upload 580cba0d575dc5afdac8439d1d13b82.jpg
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"uploadFile\"]").set_input_files(
        files=backFiles)

    # Click text=确定
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("text=确定").click()
    logger.info('上传背面')
    time.sleep(2)
    # Click input[name="custPhoto"] >> nth=2
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"custPhoto\"]").nth(2).click()

    holdUrl = postBody.holdUrl
    holdUrlResult = requests.get(holdUrl)
    holdFiles = [{"name": "手持.jpg", "mimeType": "image/jpeg", "buffer": holdUrlResult.content}]

    # Upload 3f4db6fb080f08201470b0e0d7b55a7.jpg
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"uploadFile\"]").set_input_files(
        files=holdFiles)

    # Click text=确定
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("text=确定").click()
    logger.info('上传手持')
    time.sleep(2)
    # Click #add
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("#add").click()

    # Click text=下一步
    page.locator("text=下一步").click()
    page.wait_for_url(
        "https://crm.10039.cc/crm/creatCustController/costInfo?packageName=%E4%B9%90%E4%BA%AB%E4%BA%B2%E6%83%856%E5%85%83%E5%A5%97%E9%A4%90-CMC-B")
    time.sleep(2)

    logger.info('首页下一步')

    # ---------------------
    context.close()
    browser.close()


def runPlayWRight(postBody, c):
    with sync_playwright() as playwright:
        run(playwright, postBody, c)


if __name__ == '__main__':
    config = yaml.load(
        open('config.yaml', 'r', encoding='utf-8').read(),
        yaml.SafeLoader
    )
    username = config.get('username')
    password = config.get('password')
    if username and password:
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        logger.critical('请在"config.yaml"文件中填写账号密码')
        input('按回车键退出')
