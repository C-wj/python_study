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

serialNumber = '17031813184'
tradeTypeCode = 90
base_url = 'https://crm.10039.cc'

home_url = '/crm/manager/login/login.jsp'
yzm_url = '/crm/validateCode'
login_url = '/crm/loginController/login'
upload_url = '/crm/uploadImgController/upload'
getRoutDeparts_url = '/crm/loginController/getRoutDeparts'
updateRoutDeparts_url = '/crm/loginController/updateRoutDeparts'
checkCust_url = '/crm/VCommonController/checkCust'
qryAllUserInfo_url = '/crm/VCommonController/qryAllUserInfo'
getOCR_url = '/crm/uploadImgController/getOCR'


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


def uploadImage(client, type, fileId, fileName, faceUrl):
    imageData = getUploadImageData(type, fileId, fileName)
    faceUResult = client.get(faceUrl)
    files = {'uploadFile': (fileName, faceUResult.read(), 'image/jpeg')}
    print(faceUResult)
    imageResponse = client.post(url=upload_url, data=imageData, headers=login_headers, files=files,
                                follow_redirects=False)
    print(imageResponse.json())
    return imageResponse.json()


def getUploadImageData(type, fileId, fileName):
    return {'type': type,
            'fileId': fileId,
            'localUrl': 'C:\\fakepath\\' + fileName}


def getOCR(imageBase):
    ocrData = {'base': imageBase}
    ocrResult = client.post(url=getOCR_url, data=ocrData, headers=login_headers,
                            follow_redirects=False)
    print(ocrResult.json())
    return ocrResult.json()


if __name__ == '__main__':
    # 获取登录cookie
    # login_cookie = getLoginCookie()
    login_cookie = 'SESSION=' + '602d95bf-e14b-4c69-a81e-2f3c3a7abda7' + ";" + base_cookie

    headers['Cookie'] = login_cookie

    login_headers = headers
    print(login_headers)

    with httpx.Client(base_url=base_url) as client:
        # # 获取渠道
        # data = {"departNameFilter": "上海", "sort": "province_code", "order": "asc"}
        # routR = client.post(url=getRoutDeparts_url, data=data, headers=login_headers,
        #                     follow_redirects=False)
        #
        # print(routR.json())
        # routJson = routR.json()[0]
        # provinceCode = routJson.get('province_code')
        # regionCode = routJson.get('regin_code')
        #
        # # 更新渠道
        # data = {'departName_nav': routJson.get('departName'),
        #         'regin_code_nav': regionCode,
        #         'province_code_nav': provinceCode,
        #         'regin_encode_nav': routJson.get('reginEncode'),
        #         'province_encode_nav': routJson.get('provinceEncode'),
        #         'departId_nav': routJson.get('departId')
        #         }
        #
        # updateRoutDeparts = client.post(url=updateRoutDeparts_url, data=data, headers=login_headers,
        #                                 follow_redirects=False)
        # print(updateRoutDeparts.json())
        # routJson = updateRoutDeparts.json()
        #
        # # 查询产品信息
        # checkCustSearchParam = {"provinceCode": provinceCode,
        #                         "regionCode": regionCode,
        #                         "qryMode": "0",
        #                         "serialNumber": serialNumber,
        #                         "queryType": "null",
        #                         "tradeTypeCode": "90"}
        # checkCustSearchParams = {'param': checkCustSearchParam}
        #
        # checkCustSearch = client.post(url=checkCust_url, params=checkCustSearchParams, headers=login_headers,
        #                               follow_redirects=False)
        #
        # print(checkCustSearch.json())
        #
        # # qryAllUserInfo
        # qryAllUserInfoData = {'serialNumber': serialNumber, 'tradeTypeCode': tradeTypeCode}
        # qryAllUserInfoResult = client.post(url=qryAllUserInfo_url, data=qryAllUserInfoData, headers=login_headers,
        #                                    follow_redirects=False)
        # print(qryAllUserInfoResult.json())

        # type  0 正面  1 背面  2 手持
        # 上传正面 后得到 {"fileName":"202208/agbf6e433ccde84767b98bf004f419bdd6.jpg","error":0,"url":"https://readimage.10039.cc/202208/agbf6e433ccde84767b98bf004f419bdd6.jpg","fileId":4027973,"base":1212}
        type = 0
        fileId = ''
        localUrl = 'C:\\fakepath\\' + '正面.jpg'
        # localUrl = 'C:\\fakepath\\' + '背面.jpg'
        # localUrl = 'C:\\fakepath\\' + '手持.jpg'

        faceU = 'https://oss-education.oss-accelerate.aliyuncs.com/1564153514236964866.jpg'
        faceDataResultJson = uploadImage(client, 0, '', '正面.jpg', faceU)
        fileId = faceDataResultJson.get('fileId')
        faceFileName = faceDataResultJson.get('fileName')
        faceUrl = faceDataResultJson.get('url')
        faceBase = faceDataResultJson.get('base')
        faceBase = faceBase.replace("data:image/jpeg;base64,", "")

        backUrl = 'https://oss-education.oss-accelerate.aliyuncs.com/1564176638693208065.jpg'
        backDataResultJson = uploadImage(client, 1, fileId, '背面.jpg', backUrl)
        backFileName = backDataResultJson.get('fileName')
        backUrl = backDataResultJson.get('url')
        backBase = backDataResultJson.get('base')
        backBase = backBase.replace("data:image/jpeg;base64,", "")

        holdUrl = 'https://oss-education.oss-accelerate.aliyuncs.com/1564177558235639809.jpg'
        holdDataResultJson = uploadImage(client, 2, fileId, '手持.jpg', holdUrl)
        fileId = holdDataResultJson.get('fileId')
        holdFileName = holdDataResultJson.get('fileName')
        holdUrl = holdDataResultJson.get('url')
        holdBase = holdDataResultJson.get('base')

        # OCR识别
        faceOCR = getOCR(faceBase)

    # 上传图片
    # imagePath = './正面.jpg'
    #
    # files = {'uploadFile': ('正面.jpg', open(imagePath, 'rb'), 'image/jpeg')}
    # uploadR = client.post(upload_url + '?dir=image', headers=login_headers, files=files)
    # print(uploadR)
    # print(uploadR.text)
    # login_headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # data = {"departNameFilter": "深圳", "sort": "province_code", "order": "asc"}
    # routR = client.post("https://crm.10039.cc/crm/loginController/getRoutDeparts", data=data, headers=login_headers,
    #                     follow_redirects=False)
    # print(routR)
    # print(routR.json())
