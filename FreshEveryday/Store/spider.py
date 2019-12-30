
from time import sleep
import os
import random
import requests
from lxml import etree
from urllib.request import urlretrieve
from Store.models import Goods,GoodsType

def getSpider(keywords,type_id):
    url = "https://search.jd.com/Search?keyword=%s&enc=utf-8&cid1=12218&wq=%s"%(keywords,keywords)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
    }
    params = {
        "keyword": keywords,
        "enc": "utf-8",
        "cid1": 12218,
        "wq": keywords,
        "pvid": "3f00a8fb1b73420a96431431466b4d00"
    }

    response = requests.get(url,headers = headers,params=params)
    content = response.content.decode()
    html = etree.HTML(content)
    xpath_list = html.xpath('//div[@id="J_goodsList"]/ul/li/div[@class="gl-i-wrap"]/div[@class="p-img"]/a')
    for index,x in enumerate(xpath_list,1):
        name = x.attrib["title"]
        img = "http:"+x.xpath("img")[0].attrib["source-data-lazy-img"]
        #文件的名称
        imgName = img.rsplit("/",1)[1]
        #文件的路径
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        img_path = os.path.abspath(os.path.join(path,"static/store/img/%s"%imgName))

        goods = Goods()
        goods.name = str(index).zfill(2)+keywords
        goods.store = 1
        goods.price = random.randint(20,100)
        goods.safe_data = "%s-%s-%s"%(random.randint(1000,9999),random.randint(1,12),random.randint(1,28))
        try:
            urlretrieve(img,img_path)
        except:
            continue
        else:
            goods.picture = "store/img/"+imgName
        goods.number = random.randint(100,1000)
        goods.description = name
        goods.state = 1
        goods.goods_type = GoodsType.objects.get(id=type_id)
        goods.save()

        sleep(0.5)

if __name__ == '__main__':
    task = {
        1: "西红柿、芹菜、包菜、胡萝卜、油麦菜、土豆、洋葱、白菜、白萝卜、铁棍山药",
        2: "鲍鱼、龙虾、甲鱼、大闸蟹、海带、皮皮虾、鲤鱼、海螺、鳕鱼、帝王蟹",
        3: "猪头肉、猪蹄、猪排骨、五花肉、羊腰子、羊杂、羊蝎子、牛心、牛肉、羊蹄",
        4: "鸡肉、土鸡蛋、鸭脖、鸭架、鸭蛋、鹅蛋、鹅肝、烤鸭、烧鸡、鹅掌",
        5: "汤圆、饺子、海虾、速冻猪肉、肉丸、甜不辣、蟹排、鸡块、鱿鱼排、鱼丸",
        6: "奇异果、香蕉、榴莲、苹果、山竹、椰子、葡萄、橘子、橙子、柚子"
    }























"""
from Store.models import Goods,GoodsType
task = {
    1: "西红柿、芹菜、包菜、胡萝卜、油麦菜、土豆、洋葱、白菜、白萝卜、铁棍山药",
    2: "鲍鱼、龙虾、甲鱼、大闸蟹、海带、皮皮虾、鲤鱼、海螺、鳕鱼、帝王蟹",
    3: "猪头肉、猪蹄、猪排骨、五花肉、羊腰子、羊杂、羊蝎子、牛心、牛肉、羊蹄",
    4: "鸡肉、土鸡蛋、鸭脖、鸭架、鸭蛋、鹅蛋、鹅肝、烤鸭、烧鸡、鹅掌",
    5: "汤圆、饺子、海虾、速冻猪肉、肉丸、甜不辣、蟹排、鸡块、鱿鱼排、鱼丸",
    6: "奇异果、香蕉、榴莲、苹果、山竹、椰子、葡萄、橘子、橙子、柚子"
}

goods = Goods()
goods.name = "从网上找"
goods.store = "默认1"
goods.price = 11.5
goods.safe_date = "1991-01-11"
goods.picture = "从网上找"
goods.number = 11
goods.desctiption = "从网上找"
goods.state = 1
goods.type = GoodsType.objects.get(id=1)
goods.save()
"""