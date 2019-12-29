from django.urls import path, re_path
from Store.views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'store'
urlpatterns = [
    path('base/', base),
    path('list_goods/', Goods_list),
    path('add_goods/', Goods_add, name='add_goods'),
    path('changePrice/', changePrice),
    path('changeState/', changeState),
    path('GoodsView/', csrf_exempt(GoodsView.as_view())),  # 类视图规避csrf
    path('vc/', vueContest),
    path('vgl/', vue_goods_list),
    re_path('goods/(?P<id>\d+)/', goods),
    re_path('goods_update/(?P<id>\d+)/', goods_update, name='goods_update'),
    path('GoodsType/', Goods_type),




]
