from django.shortcuts import render

# Create your views here.

def user_manage_html(request):
    if request.user.is_authenticated:
        content = {
            'username':request.user,
        }

        return render(request,'user_manage/user_manage.html',content)
    else:
        return render(request,'.html')
