from django.db import models
import django.utils.timezone as timezone
from django.conf import settings as setting
# Create your models here.
class content(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=2000)
    key_positions = models.CharField(max_length=4000, null=True, blank=True)
    create_datetime = models.DateTimeField('保存日期', default=timezone.now)
    last_update_datetime = models.DateTimeField('最后修改日期', auto_now=True, null=True, blank=True)
    last_update_user = models.IntegerField(null=True)
    cost_time = models.IntegerField(null=True)
    group_id = models.IntegerField(null=True)
    is_labeled = models.BooleanField(default=False)
    comments = models.CharField(max_length=500, null=True, blank=True)
    settings_id = models.IntegerField(null=True)
    class_list = models.CharField(max_length=200, null=True, blank=True)
    is_dirty_data = models.BooleanField(default=False)
    class Meta:
        db_table = 'fpm_content'

    def __unicode__(self):
        return self.id


class content_group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user_id = models.IntegerField(null=True, blank=True)
    create_datetime = models.DateTimeField('保存日期', default=timezone.now)
    last_update_datetime = models.DateTimeField('最后修改日期', auto_now=True, null=True, blank=True)
    last_update_user = models.IntegerField(null=True)
    is_complete = models.BooleanField(default=False)
    settings_id = models.IntegerField(null=True)
    class Meta:
        db_table = 'fpm_content_group'

    def __unicode__(self):
        return self.name


# 用户收藏的样本
class collected_content(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    content_id = models.IntegerField()
    create_datetime = models.DateTimeField('保存日期', default=timezone.now)
    last_update_datetime = models.DateTimeField('最后修改日期', auto_now=True, null=True, blank=True)
    last_update_user = models.IntegerField(null=True)

    class Meta:
        db_table = 'fpm_collected_content'

    def __unicode__(self):
        return self.name

from sample_manage.settings import MEDIA_ROOT
from datetime import date
def upload_to(instance, fielname):
    return '/'.join([MEDIA_ROOT,'doc_file', str(date.today()), fielname])

class settings(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    settings = models.CharField(max_length=500)
    comments = models.CharField(max_length=500, null=True, blank=True)
    setting_type = models.CharField(max_length=20, null=True, blank=True)
    is_single = models.BooleanField(default=False)
    doc_file_path = models.FileField(upload_to=upload_to, verbose_name="上传的文档", help_text="上传的文档",null=True)
    to_database = models.CharField(max_length=500,null=True, blank=True)
    class Meta:
        db_table = 'fpm_settings'

    def __unicode__(self):
        return self.name

class statistic_info(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=200,default="")
    group_id = models.IntegerField(null=True)
    group_name = models.CharField(max_length=200,default="")
    accuracy = models.FloatField()
    settings_id = models.IntegerField()
    database = models.CharField(max_length=2000,default="")
    accuracy_count = models.IntegerField(null=True)
    sum_count = models.IntegerField(null=True)
    class Meta:
        db_table = 'statistic_info'


def content_id_submit_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return './uploads/feedback/{0}/submit/content_id_{1}/{2}'.format(date.today(),instance.content_id, filename)

def content_id_reply_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return './uploads/feedback/{0}/reply/content_id_{1}/{2}'.format(date.today(),instance.content_id, filename)

class feedback_content(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    content_id = models.IntegerField()
    content = models.CharField(max_length=2000,null=True,blank=True)
    create_datetime = models.DateTimeField('保存日期', default=timezone.now)
    last_update_datetime = models.DateTimeField('最后修改日期', auto_now=True, null=True, blank=True)
    last_update_user = models.IntegerField(null=True,default=0)
    feedback_question = models.TextField()
    feedback_answer = models.TextField()
    feedback_file_submit = models.FileField(upload_to=content_id_submit_path, verbose_name="反馈附件", help_text="反馈附件",null=True,blank=True)
    feedback_file_reply = models.FileField(upload_to=content_id_reply_path, verbose_name="反馈附件", help_text="反馈附件",null=True,blank=True)

    class Meta:
        db_table = 'fpm_feedback_content'