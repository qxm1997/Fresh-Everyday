from django.db import models


# Create your models here.


class LoginUser(models.Model):
    username = models.CharField(max_length=32) # 全名
    email = models.EmailField()
    password = models.CharField(max_length=32)








class GoodsType(models.Model):
    type_name = models.CharField(max_length=32)
    type_pic = models.ImageField(upload_to='store/img')




class Goods(models.Model):
    name = models.CharField(max_length=128)  # 商品名
    store = models.CharField(max_length=128)  # 店铺
    price = models.FloatField()  # 价格
    safe_data = models.DateField()  # 保质期
    picture = models.ImageField(upload_to='store/img')  # 图片
    number = models.IntegerField()  # 数量
    description = models.TextField()  # 描述
    state = models.IntegerField(default=1)  # 0下架 1上架
    goods_type = models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,default=1)



