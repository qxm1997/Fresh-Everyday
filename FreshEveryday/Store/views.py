from django.shortcuts import render, HttpResponseRedirect, HttpResponse,render_to_response
from Store.models import *
from django.core.paginator import Paginator
import hashlib
from Store.forms import *


# Create your views here.


def ce(request):
    return HttpResponse('测试成功')


# 加密
def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

# def base(request):
#     cookie_email = request.COOKIES.get('email')
#     session_email = request.session.get('email')
#     if cookie_email and session_email and cookie_email == session_email:
#         return render_to_response('user/index.html', locals())  # 注意
#     else:
#         return HttpResponseRedirect('/user/login/')



def index(request):
    '''
        首页
        :param request:
        :return:
        '''
    cookie_email = request.COOKIES.get('email')
    session_email = request.session.get('email')
    if cookie_email and session_email and cookie_email == session_email:
        return render_to_response('store/index.html', locals())  # 注意
    else:
        return HttpResponseRedirect('/store/login/')
    # return redirect(request,'/user/index')


def Login(request):
    '''
    登录
    :param request:
    :return:
    '''
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = LoginUser.objects.filter(email=email).first()
        if user:
            db_password = user.password
            password = setPassword(password)
            if db_password == password:
                response = HttpResponseRedirect('/store/vgl/')
                response.set_cookie('email', user.email)
                response.set_cookie('id', user.id)
                request.session['email'] = user.email
                return response
    return render(request, 'store/login.html')


def Register(request):
    '''
    注册
    :param request:
    :return:
    '''

    if request.method == 'POST':
        user = UserForm(request.POST)
        if user.is_valid():
            data = user.cleaned_data
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            email = data.get('email')
            password = data.get('password')

            user = LoginUser()
            user.username = lastname+firstname
            user.email = email
            user.password = setPassword(password)
            user.save()
            return HttpResponseRedirect('/store/login/')
        else:
            error = user.errors
    return render(request, 'store/register.html', locals())



def Loginout(request):
    '''
    登出
    :param request:
    :return:
    '''
    response = HttpResponseRedirect('/user/login/')
    response.delete_cookie('email')
    response.delete_cookie('id')
    request.session.clear()
    return response



def forgetPassword(request):
    '''
    忘记密码
    :param request:
    :return:
    '''
    return render(request, 'store/forgot-password.html')




def Uje(request):
    result = {'data':''}
    email = request.GET.get('email')
    if email:
        user = LoginUser.objects.filter(email=email).first()
        if user:
            result['data'] = '该邮箱用户已存在，请登录！'
        else:
            result['data'] = '该邮箱可以使用！'
    return JsonResponse(result)













def base(request):
    return render(request, 'store/base.html')


def Goods_list(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    else:
        page = int(page)
    keywords = request.GET.get('keywords')
    if keywords:
        goods = Goods.objects.filter(name__contains=keywords).order_by('-safe_data')
    else:
        goods = Goods.objects.order_by('-safe_data')
    # 创建分页对象
    pageter = Paginator(goods, 3)  # 分页对象
    page_data = pageter.page(page)
    page_range = pageter.page_range
    count = pageter.count
    has_next = page_data.has_next()  # 是否有下一页
    has_previous = page_data.has_previous()  # 是否有上一页
    return render(request, 'store/goods_list.html', locals())


def Goods_add(request):
    type_list = GoodsType.objects.all()
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        price = data.get('price')
        safe_data = data.get('safe_data')
        number = data.get('number')
        description = data.get('description')
        goods_type = data.get("goods_type")
        picture = request.FILES.get('picture')

        goods = Goods()
        goods.name = name
        goods.price = price
        goods.safe_data = safe_data
        goods.number = number
        goods.description = description
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        goods.picture = picture
        goods.save()
        return HttpResponseRedirect('/store/vgl/', locals())

    return render(request, 'store/goods_add.html', locals())


from django.http import JsonResponse


def changePrice(request):
    result = {'code': 400, 'data': ''}
    goods_id = request.GET.get('goods_id')
    price = request.GET.get('price')
    if goods_id and price:
        g = Goods.objects.filter(id=goods_id).first()
        if g:
            g.price = price
            g.save()
            result['data'] = price
            result['code'] = 200
        else:
            result['data'] = '该商品不存在'
    else:
        result['data'] = '商品id或价格不存在'
    return JsonResponse(result)


def changeState(request):
    result = {'code': 400, 'data': ''}
    goods_id = request.GET.get('goods_id')
    state = request.GET.get('state')
    if goods_id and state:
        g = Goods.objects.filter(id=goods_id).first()
        if g:
            if state == 'down':
                g.state = 0
            elif state == 'up':
                g.state = 1
            g.save()
            result['data'] = '修改成功'
            result['code'] = 200
        else:
            result['data'] = '该商品不存在'
    else:
        result['data'] = '商品id或价格不存在'
    return JsonResponse(result)


from django.views import View


class GoodsView(View):
    def __init__(self, **kwargs):
        super(GoodsView, self).__init__(**kwargs)
        self.result = {
            'code': 400,
            'verson': 'v1',
            'data': [

            ]
        }

    def get(self, request):
        id = request.GET.get('id')
        if id:
            goods_list = Goods.objects.filter(id=int(id)).values()
        else:
            page = request.GET.get('page')
            if page:
                page = int(page)
            else:
                page = 1
            all_data = list(Goods.objects.all().values())
            pageter = Paginator(all_data, 25)
            goods_list = pageter.page(page).object_list
            self.result['page_range'] = list(pageter.page_range)
        self.result['data'] = list(goods_list)
        return JsonResponse(self.result, safe=False, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        method = request.method
        self.result['data'].append(method)
        return JsonResponse(self.result)

    def put(self, request):
        method = request.method
        self.result['data'].append(method)
        return JsonResponse(self.result)

    def delete(self, request):
        method = request.method
        self.result['data'].append(method)
        return JsonResponse(self.result)


def vueContest(request):
    return render(request, 'store/vue.html')


def vue_goods_list(request):
    return render(request, 'store/vue_goods_list.html')


def goods(request, id):
    return render(request, 'store/goods.html', locals())


def goods_update(request, id):
    if request.method == "POST":
        id = request.POST.get("id")
        name = request.POST.get("name")
        price = request.POST.get("price")
        safe_data = request.POST.get("safe_data")
        number = request.POST.get("number")
        description = request.POST.get("description1")
        goods_type = request.POST.get("goods_type")
        picture = request.FILES.get("picture")

        goods = Goods.objects.get(id=int(id))
        goods.name = name
        goods.price = price
        goods.safe_data = safe_data
        goods.number = number
        goods.description = description
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        if picture:
            goods.picture = picture
        goods.save()
        response = HttpResponseRedirect("/store/goods/%s/" % id, locals())
        return response
    return render(request, "store/goods_update.html", locals())


def Goods_type(request):
    dic_list = {'data': ''}
    goods_list = GoodsType.objects.all().values()
    dic_list['data'] = list(goods_list)
    return JsonResponse(dic_list)


from Store.spider import getSpider
def getData(request):

    task = {
        1: "西红柿、芹菜、包菜、胡萝卜、油麦菜、土豆、洋葱、白菜、白萝卜、铁棍山药",
        2: "奇异果、香蕉、榴莲、苹果、山竹、椰子、葡萄、橘子、橙子、柚子",
        3: "鲍鱼、龙虾、甲鱼、大闸蟹、海带、皮皮虾、鲤鱼、海螺、鳕鱼、帝王蟹",
        4: "猪头肉、猪蹄、猪排骨、五花肉、羊腰子、羊杂、羊蝎子、牛心、牛肉、羊蹄",
        5: "鸡肉、土鸡蛋、鸭脖、鸭架、鸭蛋、鹅蛋、鹅肝、烤鸭、烧鸡、鹅掌",
        6: "汤圆、饺子、海虾、速冻猪肉、肉丸、甜不辣、蟹排、鸡块、鱿鱼排、鱼丸",
    }
    for t in task:
        for k in task[t].split("、"):
            getSpider(k,t)
    return HttpResponse("1111")
