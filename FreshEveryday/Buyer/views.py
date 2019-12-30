from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from Store.models import GoodsType,Goods
from django.core.paginator import Paginator
from User.models import *
from User.views import setPassword

# Create your views here.

def loginValid(fun):
    def inner(request,*args,**kwargs):
        cookie_email = request.COOKIES.get("user_email")
        cookie_id = request.COOKIES.get("user_id")
        session_eamil = request.session.get('user_email')
        session_id = request.session.get('user_id')
        if cookie_email and cookie_id and session_eamil and session_id  and cookie_email==session_eamil:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/buyer/login/')
    return inner


def register(request):
    #User视图李创建的
    return render(request, 'buyer/register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        user = Quser.objects.filter(email=email).first()
        if user:
            db_password = user.password
            password = setPassword(password)
            if db_password == password:
                response = HttpResponseRedirect("/")
                response.set_cookie('user_id', user.id)
                response.set_cookie('user_email', user.email)
                request.session['user_id'] = user.id
                request.session['user_email'] = user.email
                return response
    return render(request,'buyer/login.html')


def logout(request):
    request.session.clear()
    response = HttpResponseRedirect("/")
    response.delete_cookie("user_id")
    response.delete_cookie("user_email")
    return response






def index(request):
    type_list = GoodsType.objects.all()
    return render(request,'buyer/index.html',locals())

def detail(request):

    id = request.GET.get('id')
    goods = Goods.objects.filter(id=id).first()
    return render(request,'buyer/detail.html',locals())


def goods_list(request):
    type_id = request.GET.get("type_id")
    keywords = request.GET.get('keywords')
    page = request.GET.get("page", 1)
    goodList = Goods.objects.filter(state=1)
    if type_id:
        goodsType = GoodsType.objects.filter(id=int(type_id)).first()
        if goodsType:
            goodList = goodsType.goods_set.filter(state=1)
    if keywords and keywords != 'None':
        goodList = Goods.objects.filter(name__contains=keywords,state=1)

    #分页
    # paginator = Paginator(goodList, 25)
    # page_data = paginator.page(int(page))





    if len(goodList)>0:
        paginator = Paginator(goodList, 25)
        page_data = paginator.page(int(page))
        page_range = paginator.page_range
        count = paginator.count
        page_num = paginator.num_pages
        num_pages = paginator.num_pages
        has_next = page_data.has_next()
        has_previous = page_data.has_previous()
        previous = int(page)-1
        next = int(page)+1
    else:
        page_data=[]
    return render(request,"buyer/list.html",locals())

@loginValid
def address(request):
    user_id = request.COOKIES.get('user_id') #cookie当中的用户id
    user = Quser.objects.get(id = int(user_id)) #获取用户信息
    #获取用户所有地址
    address_list = user.address_set.all()
    now_address = user.address_set.filter(is_now=1).first()

    #请求保存
    if request.method == "POST":
        recver = request.POST.get("recver")
        address = request.POST.get("address")
        post_code = request.POST.get("post_code")
        phone = request.POST.get("phone")

        addr = Address()
        addr.recver = recver
        addr.address = address
        addr.post_code = post_code
        addr.phone = phone
        addr.user = Quser.objects.get(id = user_id)
        addr.save()

    return render(request,"buyer/user_center_site.html",locals())

@loginValid
def setDefaultAddress(request):
    user_id = request.COOKIES.get("user_id") #拥有登录才会有效

    address_id = int(request.GET.get("id")) #获取将要被设为默认地址的地址
    # address_id = request.GET.get("id")
    user = Quser.objects.get(id=int(user_id)) #获取用户
    address_list = user.address_set.all() #获取用户所有地址
    address_list.update(is_now=0) #讲默认去除

    address = Address.objects.get(id=address_id) #设置新的默认
    address.is_now = 1
    address.save()

    return HttpResponseRedirect("/buyer/address/")

@loginValid
def add_cart(request):
    user_id = request.COOKIES.get("user_id")  # 拥有登录才会有效
    user = Quser.objects.get(id=int(user_id))  # 获取用户
    goods_number = request.POST.get("goods_number")
    goods_id = request.POST.get("goods_id")
    goods = Goods.objects.get(id=int(goods_id))

    buyCar = BuyCar()
    buyCar.goods_name = goods.name
    buyCar.goods_price = goods.price
    buyCar.goods_total = goods.price * int(goods_number)
    buyCar.goods_number = int(goods_number)
    buyCar.goods_picture = goods.picture
    buyCar.goods_store = goods.store
    buyCar.user = user
    buyCar.save()

    return JsonResponse({"data": "保存成功"})
@loginValid
def cart(request):
    user_id = request.COOKIES.get("user_id")  # 拥有登录才会有效
    user = Quser.objects.get(id=int(user_id))
    goods_list =user.buycar_set.all()
    return render(request,'buyer/cart.html',locals())

@loginValid
def palce_order(request):
    user_id = request.COOKIES.get('user_id')
    user = Quser.objects.get(id=int(user_id))
    address = user.address_set.filter(is_now=1).first()
    goods_list = []
    if request.method == 'POST':
        goods_id = request.POST.getlist('cart_goods')
        goods_list = [BuyCar.objects.get(id=int(id)) for id in goods_id]
    return render(request, 'buyer/place_order.html', locals())
from Buyer.AliPay import aliPay
import time

@loginValid
def save_order(request):
    user_id = request.COOKIES.get('user_id')
    user = Quser.objects.get(id=int(user_id))
    if request.method == 'POST':
        address_id = request.POST.get('addr_id')
        cart_id = request.POST.getlist('car_id')
        time_str = str(time.time()).replace('.',address_id)


        #保存订单总表
        pay_order = PayOrder()
        pay_order.pay_number = time_str
        pay_order.pay_status=1
        pay_order.goods_total = len(cart_id)-1
        pay_order.user = user
        pay_order.address = Address.objects.get(id=int(address_id))
        pay_order.save()

        #保存订单详情表
        pay_total = 0
        for id in cart_id:
            if id.isdigit():
                cart_goods = BuyCar.objects.get(id=int(id))
                pay_info = PayInfo()
                pay_info.goods_name = cart_goods.goods_name
                pay_info.goods_price = cart_goods.goods_price
                pay_info.goods_number = cart_goods.goods_number
                pay_info.goods_total = cart_goods.goods_total
                pay_info.goods_picture = cart_goods.goods_picture
                pay_info.goods_store = cart_goods.goods_store
                pay_info.pay_status = 1
                pay_info.order_id = pay_order
                pay_info.save()

                pay_total += cart_goods.goods_total

                # 保存订单总价
                pay_order.pay_price = pay_total
                pay_order.save()

        pay_url = aliPay(pay_order.pay_number, pay_total)
        result = {"state": "success", "pay_url": pay_url}
    else:
        result = {"state": "error", "pay_url": ""}
    return JsonResponse(result)


@loginValid
def hhh(request):
    order_id = request.GET.get("out_trade_no")
    payorder = PayOrder.objects.get(pay_number=order_id)
    payorder.pay_status = 2
    payorder.save()
    payorder.payinfo_set.all().update(pay_status = 2)
    return render(request,"buyer/hhh.html",locals())