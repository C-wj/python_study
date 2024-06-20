from urllib.parse import quote

import requests
from flask import Flask, request, jsonify, render_template_string

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
    html_form = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trigger Script</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f0f0;
            }
            .container {
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                max-width: 400px;
                width: 100%;
            }
            h1 {
                font-size: 24px;
                margin-bottom: 20px;
                text-align: center;
            }
            label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            select, input {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 4px;
                box-sizing: border-box;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                font-size: 16px;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            #response {
                margin-top: 20px;
            }
        </style>
        <script>
            function updateEndItem() {
                var startItem = document.getElementById("start_item").value;
                document.getElementById("end_item").value = startItem;
            }

            function submitForm(event) {
                event.preventDefault(); // 阻止表单的默认提交行为
                var form = document.getElementById('triggerForm');
                var formData = new FormData(form);

                fetch('/trigger', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    var responseDiv = document.getElementById('response');
                    responseDiv.innerHTML = '<h2>Response Data</h2>';
                    data.forEach(item => {
                        responseDiv.innerHTML += '<p>Item: ' + item.item + ', Response: ' + item.response + '</p>';
                    });
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Trigger Script</h1>
            <form id="triggerForm" onsubmit="submitForm(event)">
                <label for="uid">UID:</label>
                <select id="uid_select" name="uid" onchange="document.getElementById('uid_input').value = this.value;">
                    <option value="智能人机1号" selected>智能人机1号</option>
                    <option value="智能人机2号">智能人机2号</option>
                    <option value="智能人机3号">智能人机3号</option>
                </select>
                <input type="text" id="uid_input" name="uid" value="智能人机1号"><br><br>
    
                <label for="start_item">Start Item:</label>
                <select id="start_item_select" onchange="document.getElementById('start_item').value = this.value; updateEndItem();">
                    <option value="9005"> 9005 寰宇护符 </option>
                    <option value="25646">25646 神器材料礼盒（鸿蒙圣珠，天火液，涣神沙） </option>
                    <option value="25649">25649 令牌天赐随机 </option>
                    <option value="25689 ">25689 高阶技能书  </option>
                    <option value="25700">25700 法宝精华礼袋 </option>
                    <option value="25821">25821 五星魂器 </option>
                    <option value="25852">25852 配饰宝箱 (4星)</option>
                    <option value="25853">25853 配饰宝箱 (5星)</option>
                    <option value="25988">25988 法宝精华自选 </option>
                    <option value="25856">25856 铸灵礼盒 (4星)</option>
                    <option value="25857">25857 铸灵礼盒 (5星)</option>
                    <option value="25607">25607 稀有宠自选蛋</option>
                    <option value="25608">25608 稀有宠自选蛋+2  </option>
                    <option value="25688">25688 五星神印  </option>
                    <option value="25676">25676 法宝 1</option>
                    <option value="25677">25677 法宝 2</option>
                    <option value="25678">25678 法宝 3</option>
                    <option value="25606">25606 天赐令牌自选盒 </option>
                </select>
                <input type="number" id="start_item" name="start_item" value="9005"><br><br>
    
                <label for="end_item">End Item:</label>
                <select id="end_item_select" onchange="document.getElementById('end_item').value = this.value;">
                    <option value="9005"> 9005 寰宇护符 </option>
                    <option value="25646">25646 神器材料礼盒（鸿蒙圣珠，天火液，涣神沙） </option>
                    <option value="25649">25649 令牌天赐随机 </option>
                    <option value="25689 ">25689 高阶技能书  </option>
                    <option value="25700">25700 法宝精华礼袋 </option>
                    <option value="25821">25821 五星魂器 </option>
                    <option value="25852">25852 配饰宝箱 (4星)</option>
                    <option value="25853">25853 配饰宝箱 (5星)</option>
                    <option value="25988">25988 法宝精华自选 </option>
                    <option value="25856">25856 铸灵礼盒 (4星)</option>
                    <option value="25857">25857 铸灵礼盒 (5星)</option>
                    <option value="25607">25607 稀有宠自选蛋</option>
                    <option value="25608">25608 稀有宠自选蛋+2  </option>
                    <option value="25688">25688 五星神印  </option>
                    <option value="25676">25676 法宝 1</option>
                    <option value="25677">25677 法宝 2</option>
                    <option value="25678">25678 法宝 3</option>
                    <option value="25606">25606 天赐令牌自选盒 </option>
                </select>
                <input type="number" id="end_item" name="end_item" value="9005"><br><br>
    
                <label for="num">Num:</label>
                <input type="number" id="num" name="num" value="1"><br><br>
    
                <input type="submit" value="Trigger">
            </form>
        <div id="response"></div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_form)


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

        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=payload)

        # 将响应文本转换为中文
        response_text = response.text.encode('latin1').decode('unicode_escape')

        # 打印响应内容
        responses.append({'item': item, 'response': response_text})

    return jsonify(responses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
