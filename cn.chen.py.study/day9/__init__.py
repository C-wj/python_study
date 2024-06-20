import requests

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

# 定义payload模板  type=charge2&checknum=123456&uid=%E5%8C%97%E9%83%AD%E7%BA%AF%E7%86%99&num=22&qu=1
#  num 11-物品
#  num 22-材料
#  num 33-碎片
#  num 44-补给品
#  num 55-图鉴
#  num 66-仓库
#  num 77-宠物
# payload_template = "type=mail&checknum=123456&uid=%E5%8C%97%E9%83%AD%E7%BA%AF%E7%86%99&item={item}&num=99&qu=1"
payload_template = "type=mail&checknum=123456&uid=%E9%99%88%E5%B9%B3%E5%AE%89&item={item}&num={num}&qu=1"

# 64599 技能书 550 神龙皮肤 561-570 行动丹 581-590 技能书 530-550 幻兽蛋
# 25000 - 25199 觉醒石 25565-200万经验丹 25566 超级技能书 5567 法宝精华  5568 令牌自选 25569 究极造化丹 25586 元宝
# 25586<x< 25600 没用 |  600- 700 宠物蛋称号神印技能书 | 25700 - 25800 紫装+称号 | 800-900 称号 皮肤 命格卡 | 900-1000 时装 宠物蛋
# 26001- 26200 材料 200-499 灵骑饰品 500-700 卡片 700-999 材料
# 27000-27160 任务道具 160-200 装备图纸 碎片 27190神兽碎片 450-500 觉醒石 500 - 600 活动材料 700心法
# 28112 皮肤  28110 铜币 15w  138~14 146 命格礼包  28160铜币礼包 28161·162声望卡  170~190 垃圾礼包 28228 宠物蛋
# 28448 ~28462  28924~28926称号衣服
# 31618 八星剁椒鱼头
#
# item值的范围
start_item = 28110
end_item = 28110
num = 3

# 循环调用
for item in range(start_item, end_item + 1):
    # 构造payload字符串
    payload = payload_template.format(item=str(item).zfill(5), num=str(num))

    # 发送POST请求
    response = requests.post(url, headers=headers, data=payload)

    # 打印响应内容
    print(f"Response for item {item}: {response.text}")
