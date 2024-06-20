from urllib.parse import quote

import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

url = "http://211.101.237.202:82/ht/user/gmquery.php"

# 定义headers字典
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': '211.101.237.202:82',
    'Origin': 'http://211.101.237.202:82',
    'Referer': 'http://211.101.237.202:82/ht/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'PHPSESSID=n5o1r7s41k1pm2h6je0i68d2le;uid=20;token=3569baab-a465-41a6-a583-18ec16122f70',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}
payload_template = "type=mail&checknum=123456&uid={uid}&item={item}&num={num}&qu=1"


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/trigger', methods=['POST'])
def trigger():
    uid = request.form.get('uid')
    start_item = int(request.form.get('start_item'))
    end_item = int(request.form.get('end_item'))
    num = int(request.form.get('num'))

    # 将 UID 转换为 URL 编码
    uid_urlencoded = quote(uid)

    responses = []

    for item in range(start_item, end_item + 1):
        # 构造 payload 字符串
        payload = payload_template.format(item=str(item).zfill(5), num=str(num), uid=uid_urlencoded)
        print(payload)
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=payload)

        # 将响应文本转换为中文
        response_text = response.text.encode('latin1').decode('unicode_escape')

        # 打印响应内容
        responses.append({'item': item, 'response': response_text})

    return jsonify(responses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
