from django.shortcuts import render, HttpResponse
from Store.models import GoodsType

# Create your views here.
def register(request):
    return render(request, 'buyer/register.html')


def login(request):
    return HttpResponse('这是登录页')

def index(request):
    type_list = GoodsType.objects.all()
    return render(request,'buyer/index.html',locals())


