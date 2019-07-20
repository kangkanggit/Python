from django.shortcuts import render,render_to_response,redirect
from Login.models import Login_User
from django.http import JsonResponse,HttpResponseRedirect
import hashlib
#密码加密
def setPassword(password):
    #对密码进行加密
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

#测试模板页面
def base(request):
    return render(request,'base.html')#用于测试
# Create your views here.

#主页面
def index(request):
    username = request.COOKIES.get('username')  # 获取穿过来的cookie
    session_user = request.session.get('username')  # 获取session
    if username and session_user:
        user = Login_User.objects.filter(username=username).first()
        if user and username == session_user:
            return render(request,'index.html',locals())#返回主页面
    # return render(request,'Login.html')
    return HttpResponseRedirect('/login/')#指向路径
#登录页面
def login(request):
    result = {'content':''}
    if request.method == "POST":
        username = request.POST.get('username')#获取前端变量
        password = request.POST.get('password')#获取前端变量
        if username and password:#判断存在
            user = Login_User.objects.filter(username=username).first()#从数据库查找
            if user :
                if setPassword(password) == user.password:#对比变量
                    response = HttpResponseRedirect('/index/')
                    response.set_cookie('username',username)#生成cookie
                    request.session['username'] = user.username#生成session
                    return response
                else:
                    result['content'] = '密码错误'
            else:
                result['content'] = '用户名不存在'

    return render(request,'Login.html')

#注册页面
def regiester(request):
    result = {'content': ''}
    if request.method == "POST":
        username = request.POST.get('username')#获取前端变量
        password = request.POST.get('password')#获取前端变量
        if username and password:
            user =Login_User.objects.filter(username=username).first()#从数据库查找
            if user:
                result['content'] = '用户名重复不可用'
            else:
                user = Login_User()#保存数据
                user.username = username
                user.password = setPassword(password)#对比变量
                user.save()#保存到数据库
                return redirect('/login/')#返回注册页面
        else:
            result['content'] = '用户密码不可为空'
    return render(request, 'regiester.html', locals())

#ajax的后台验证
def ajax_register(request):
    result = {'status':'error','content':''}
    username = request.GET.get('username')#获取前端的值
    if username :
        user = Login_User.objects.filter(username=username).first()#去数库中查找
        if user:
            result['content'] = '用名重复'#判断用户
        else:
            result['content'] = '用户名可以用'
            result['status'] = 'success'
    else:
            result['content'] = '用户名或密码不可以为空'
    return JsonResponse(result)#结果返回到前端


#退出页面
def out_login(request):
    response = HttpResponseRedirect('/login/')#返回到登录页面
    response.delete_cookie('username')#删除cookie
    return response


