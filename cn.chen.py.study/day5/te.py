qryAllUserInfoResult = "{'result': {'remark': '身份证正反面颠倒，请确认', 'state': 'False'}, 'respDesc': '请求ocr接口异常！', 'respCrmCode': 'crm0002', 'resCode': '0000', 'resMsg': '处理成功', 'respCode': '9999'}"

if __name__ == '__main__':
    qryAllUserInfoResult = eval(qryAllUserInfoResult)
    result = qryAllUserInfoResult.get("result")
    # successForResponse = result.get("state")
    successForResponse = False if result.get("state") == 'false' or result.get("state") == 'False' else True
    msg = result.get("remark")
    if successForResponse:
        print("1")
    else:
        print(2)
