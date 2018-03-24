from django.shortcuts import redirect
from django.shortcuts import render
from .models import content as Content,content_group as ContentGroup,settings as Settings
def sample_delete_api(request):
    if request.method =='POST':
        print(request.POST)
        if 'settings_id' not in  request.POST:
            content = {
                'err':'请选择settings_id'
            }
            return render(request, 'sample_manage/sample_delete.html',content)
        settings_id = request.POST['settings_id']
        from django.conf import settings
        database_list = []
        for database_name in settings.DATABASES.keys():
            if database_name!='default':
                database_list.append(database_name)

        for db in database_list:
            Content.objects.using(db).filter(settings_id=settings_id).delete()
            ContentGroup.objects.using(db).filter(settings_id=settings_id).delete()
            Settings.objects.using(db).filter(id=settings_id).delete()


        return redirect('/sample_manage/sample_delete_html')