from django.shortcuts import render, HttpResponse,redirect
from django.db import connection
from app01 import models
from django import forms
from app01.part import Pagination

# Create your views here.
def depart_list(request):
    """
    部门列表
    """
    #从数据库中获取数据
    queryset =models.Department.objects.all()

    return render(request,'depart_list.html',{'queryset':queryset})
def depart_add(request):
    """
    添加部门
    """
    if request.method == 'GET':
        return render(request,'depart_add.html')
    title=request.POST.get('title')
    #空值判断
    if not title:
        return render(request,'depart_add.html',{'title_error':'部门名称不能为空'})
    sql_select="select title from app01_department where title='%s'"%title
    result=sql(sql_select)
    if result:
        return render(request,'depart_add.html',{'title_error1':'部门名称已存在'})


    models.Department.objects.create(title=title)
    #重定向
    return redirect('/depart/list/')

def depart_delete(request):
    """
    删除部门
    """
    sql="delete from app01_department where id=%s"
    pk=request.GET.get('nid')
    models.Department.objects.filter(id=pk).delete()
    return redirect('/depart/list/')
def depart_edit(request,nid):
    """
    编辑部门
    """
    sql="update app01_department set title=%s where id=%s"

    if request.method == 'GET':
        obj=models.Department.objects.filter(id=nid).first()
        return render(request,'depart_edit.html',{'obj':obj})

    title=request.POST.get('title')

    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')

def user_list(request):
    queryset=models.UserInfo.objects.all()

    '''
    for obj in queryset:      
        print(obj.id,obj.name,obj.accont,obj.creat_time.strftime('%Y-%m-%d'),obj.get_gender_display(),obj.depart_id,obj.depart.title)
    '''

    return render(request,'user_list.html',{'queryset':queryset})
def user_add(request):
    if request.method == 'GET':

        context={
            'gender_choices':models.UserInfo.gender_choices,
            'depart_list':models.Department.objects.all()
        }

        return render(request,'user_add.html',context)
    user= request.POST.get('user')
    pwd=request.POST.get('pwd')
    age=request.POST.get('age')
    ac=request.POST.get('ac')
    ctime=request.POST.get('ctime')
    gd=request.POST.get('gd')
    dp=request.POST.get('dp')
    if not user:
        return render(request,'user_add.html',{'user_error':'用户名不能为空'})
    if not pwd:
        return render(request,'user_add.html',{'pwd_error':'密码不能为空'})
    if not age:
        return render(request,'user_add.html',{'age_error':'年龄不能为空'})
    # 添加到数据库中
    models.UserInfo.objects.create(name=user, password=pwd, age=age,
                                   account=ac, creat_time=ctime,
                                   gender=gd, depart_id=dp)
    # 返回到用户列表页面
    return redirect("/user/list/")
def user_edit(request,nid):
    """
    编辑部门
    :param request:
    :return:
    """
    sql="update app01_department set title=%s where id=%s"

    if request.method == 'GET':
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        obj=models.UserInfo.objects.filter(id=nid).first()

        return render(request,'user_edit.html',{'obj':obj,'gender_choices': models.UserInfo.gender_choices,'depart_list': models.Department.objects.all()})
    user= request.POST.get('user')
    pwd=request.POST.get('pwd')
    age=request.POST.get('age')
    ac=request.POST.get('ac')
    ctime=request.POST.get('ctime')
    gd=request.POST.get('gd')
    dp=request.POST.get('dp')


    models.UserInfo.objects.filter(id=nid).update(name=user, password=pwd, age=age,
                                   account=ac, creat_time=ctime,
                                   gender=gd, depart_id=dp)
    return redirect('/user/list/')

def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')



def prettynum_list(request):
    """ 靓号列表 """
    sql("select * from app01_prettynum")
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict)

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'prettynum_list.html', context)


def sql(dir):
    sqlstr="%s"%dir


    def dict_fetchall(cursor):  # cursor是执行sql_str后的记录，作入参
        columns = [col[0] for col in cursor.description]  # 得到域的名字col[0]，组成List
        return [
            dict(zip(columns, row)) for row in cursor.fetchall()  #
        ]

    with connection.cursor() as cursor:
        cursor.execute(sqlstr)
        dataInfo = dict_fetchall(cursor)  # 调用上面的dict_fetchall()方法
    return dataInfo

def try_sql(request):
    a="select user_name.name, password, age ,account,level from app01_prettynum,app01_userinfo,user_name where app01_prettynum.mobile=user_name.mobile and app01_userinfo.name=user_name.name"
    sql1=sql(a)
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["id__contains"] = search_data
        queryset = models.PrettyNum.objects.filter(**data_dict)
    print(sql1)
    return render(request,'try.html',{'queryset':sql1})
class PrettyModelForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = "__all__"


def classfy(request):
    a="select level, avg(price) as price from app01_prettynum group by level having avg(price)>20"
    sql1=sql(a)
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["id__contains"] = search_data
        queryset = models.PrettyNum.objects.filter(**data_dict)
    print(sql1)
    return render(request,'classfy.html',{'queryset':sql1})
def view(request):
    a="select * from parent_child"
    b="select * from employee_salary"
    sql1=sql(a)
    sql2=sql(b)
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["id__contains"] = search_data
        queryset = models.PrettyNum.objects.filter(**data_dict)

    return render(request,'view.html',{'queryset':sql1,'queryset1':sql2})
def nest(request):

    a="select id ,salary.name,age,account,gender from app01_userinfo,salary where app01_userinfo.name=salary.name and salary.name in (select name from relationship)"

    sql1=sql(a)
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["id__contains"] = search_data
        queryset = models.PrettyNum.objects.filter(**data_dict)
    print(sql1)
    return render(request,'nest.html',{'queryset':sql1})

