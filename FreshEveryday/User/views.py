from django.shortcuts import render,HttpResponseRedirect
from User.models import *
import hashlib
# Create your views here.

def setPassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result




def registerQuser(request):
    referer = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        redirect_url = request.POST.get('redirect_url')

        user = Quser()
        user.username = username
        user.email = email
        user.password = setPassword(password)
        user.save()
        return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponseRedirect('/404/')



def loginQuer(request):
    pass
