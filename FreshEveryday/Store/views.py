from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from Store.models import *
from django.core.paginator import Paginator


# Create your views here.
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
            pageter = Paginator(all_data, 3)
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
