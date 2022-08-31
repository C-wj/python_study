import time

import requests
from playwright.sync_api import Playwright, sync_playwright

yzm_url = 'https://crm.10039.cc/crm/validateCode'
ocr_url = 'http://192.168.1.91:9898/ocr/file'

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

cookie = ['login_sms_zhangwenrui=1']


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, channel='chrome',
                                         args=['--disable-blink-features=AutomationControlled'], slow_mo=500)
    context = browser.new_context()
    context.add_init_script(path='stealth.min.js')
    context.add_cookies(
        cookies=[{'name': 'login_sms_zhangwenrui', 'value': '1', 'path': '/', 'domain': 'crm.10039.cc'}])

    # Open new page
    page = context.new_page()

    # Go to https://crm.10039.cc/crm/manager/login/login.jsp
    page.goto("https://crm.10039.cc/crm/manager/login/login.jsp")

    cookies = context.cookies()
    cookiesFor = ''
    for cookie in cookies:
        cookiesFor += cookie.get('name') + '=' + cookie.get('value') + ';'
    print(cookiesFor)

    headers['Cookie'] = cookiesFor
    yzmResult = requests.get(yzm_url, headers=headers)
    print(yzmResult.content)
    yzmFile = {'image': yzmResult.content}
    res = requests.post(ocr_url, files=yzmFile, timeout=4)

    # Fill [placeholder="请输入工号"]
    page.locator("[placeholder=\"请输入工号\"]").fill("zhangwenrui")

    # Fill [placeholder="请输入密码"]
    page.locator("[placeholder=\"请输入密码\"]").fill("Abc1234")

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
    page.locator("[placeholder=\"渠道名称\"]").fill("上海")

    # Click text=  <input type="button" id="" onclick="onclic()" value="查询" class="form_sub_2">
    page.click("//input[@onclick=\"onclic()\"]")

    # 选中 <tr datagrid-row-index="0" class="datagrid-row">
    #       <td field="departName">
    #           <div style="width:1782px;text-align:left;white-space:normal;height:auto;" class="datagrid-cell ">杭州大坝科技有限公司_上海</div>
    #       </td>
    # <tr datagrid-row-index="0" class="datagrid-row datagrid-row-selected">
    #  //*[@id="newForm"]/div/div/div/div/div[2]/div[2]/table/tbody/tr[1]
    #  //tr[@datagrid-row-index][1]
    # Click .datagrid-view2 > .datagrid-body
    print('查询点击1')
    page.click('.datagrid-view2 > .datagrid-body')
    print('查询点击2')
    # Click span:has-text("确定") >> nth=0

    # page.click("//*[@id=\"newDialog\"]/div[2]/a[1]/span/span")
    # page.locator("span:has-text(\"确定\")").first.click()

    # Click a:has-text("确定")
    page.click("//span[text()=\"确定\"][@class=\"l-btn-text\"]")

    # Click input[name="identityNum"]
    page.locator("input[name=\"identityNum\"]").click()

    # Fill input[name="identityNum"]
    page.locator("input[name=\"identityNum\"]").fill("16518210274")

    # Click input[name="button"]
    page.locator("input[name=\"button\"]").click()

    # Click text=下一步
    page.locator("text=下一步").click()
    page.wait_for_url(
        "https://crm.10039.cc/crm/costomerDataReverseController/costomerDataReverseRedirect?serialNumber=16518210274&packageKindCode=X001LXTC&tradeTypeCode=90")

    time.sleep(2)

    # Click text=新建客户
    page.locator("text=新建客户").click()

    # Click input[name="custPhoto"] >> nth=0
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"custPhoto\"]").first.click()
    faceUrl = 'https://oss-education.oss-accelerate.aliyuncs.com/1564153514236964866.jpg'
    faceUResult = requests.get(faceUrl)
    faceFiles = [{"name": "正面.jpg", "mimeType": "image/jpeg", "buffer": faceUResult.content}]
    # Upload 1a8cd62204730ce7399f8e51ff01eb0.jpg
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"uploadFile\"]").set_input_files(
        files=faceFiles)
    time.sleep(2)
    # Click text=确定
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("text=确定").click()

    # Click input[name="custPhoto"] >> nth=1
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"custPhoto\"]").nth(1).click()

    backUrl = 'https://oss-education.oss-accelerate.aliyuncs.com/1564176638693208065.jpg'
    backResult = requests.get(backUrl)
    backFiles = [{"name": "背面.jpg", "mimeType": "image/jpeg", "buffer": backResult.content}]

    # Upload 580cba0d575dc5afdac8439d1d13b82.jpg
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"uploadFile\"]").set_input_files(
        files=backFiles)
    time.sleep(2)
    # Click text=确定
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("text=确定").click()

    # Click input[name="custPhoto"] >> nth=2
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"custPhoto\"]").nth(2).click()

    holdUrl = 'https://oss-education.oss-accelerate.aliyuncs.com/1564177558235639809.jpg'
    holdUrlResult = requests.get(holdUrl)
    holdFiles = [{"name": "背面.jpg", "mimeType": "image/jpeg", "buffer": holdUrlResult.content}]

    # Upload 3f4db6fb080f08201470b0e0d7b55a7.jpg
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("input[name=\"uploadFile\"]").set_input_files(
        files=holdFiles)
    time.sleep(2)
    # Click text=确定
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("text=确定").click()

    # Click #add
    page.frame_locator("iframe[name=\"xubox_iframe1\"]").locator("#add").click()

    # Click text=下一步
    page.locator("text=下一步").click()
    page.wait_for_url(
        "https://crm.10039.cc/crm/creatCustController/costInfo?packageName=%E4%B9%90%E4%BA%AB%E4%BA%B2%E6%83%856%E5%85%83%E5%A5%97%E9%A4%90-CMC-B")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
