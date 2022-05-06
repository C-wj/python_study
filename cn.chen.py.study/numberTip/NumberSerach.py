import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

if __name__ == '__main__':
    kw = input('请输入要查询的手机号码:')

    param = {
        'q': kw
    }

    sou_SoGou = 'http://s1.cscmjc.com/api/wap/sogouwap.php'

    sou_360 = 'http://s1.cscmjc.com/api/wap/souswap360.php'
    sou_Slb = 'http://s2.cscmjc.com/api/pc/souslb.php'
    sou_baidu = 'http://s2.cscmjc.com/api/pc/sousbaidu.php'
    sou_dianHuaBang = 'http://s2.cscmjc.com/api/pc/phonenumber.php'
    sou_114 = 'http://s2.cscmjc.com/api/pc/114best.php'
    sou_7 = 'http://s2.cscmjc.com/api/pc/sous_7.php'
    sou_8 = 'http://s2.cscmjc.com/api/pc/sous_8.php'
    sou_9 = 'http://s2.cscmjc.com/api/pc/sous_9.php'
    sou_10 = 'http://s2.cscmjc.com/api/pc/sous_10.php'
    sou_11 = 'http://s2.cscmjc.com/api/pc/sous_11.php'
    sou_12 = 'http://s2.cscmjc.com/api/pc/sous_12.php'
    sou_13 = 'http://s2.cscmjc.com/api/pc/sous_13.php'
    sou_14 = 'http://s2.cscmjc.com/api/pc/sous_14.php'
    sou_15 = 'http://s2.cscmjc.com/api/pc/sous_15.php'
    sou_16 = 'http://s2.cscmjc.com/api/pc/sous_16.php'

    saoRao_imgUrl = 'https://www.guishudi.com/dhpic/0F82FA1D942FBCCA2F.gif'

    urlList = [sou_SoGou, sou_360, sou_Slb, sou_baidu, sou_dianHuaBang, sou_114, sou_7, sou_8, sou_9, sou_10, sou_11,
               sou_12, sou_13, sou_14, sou_15, sou_16]
    # urlList = [sou_114]
    key = kw + '\n'
    for url in urlList:
        mark = '标记平台：{},标记内容：{}\n'
        try:
            response = requests.get(url=url, params=param, headers=headers, timeout=4)
            page_text = response.text
            tree = etree.HTML(page_text)
            markStatusList = tree.xpath("//tr/td/text()")
            i = 0
            for markStatus in markStatusList:
                if markStatus == '标记未知':
                    continue
                markPlatform = tree.xpath("//tr/td[1]/text()")[i]
                markContent = tree.xpath("//tr/td[2]/text()")[i]
                key += mark.format(markPlatform, markContent)
                i = i + 1
        except Exception as e:
            print(e)
    print(key)
