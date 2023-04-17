from django.db import models
import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver





class User(AbstractUser):
    name=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,null=True)
    phone=models.CharField(max_length=100,null=True)
    whatsapp=models.CharField(max_length=100,null=True)
    delivery=models.DateField(null=True)
    security=models.CharField(max_length=30,null=True)
    updated_on=models.DateTimeField(auto_now=True)

class job(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    executed=models.BooleanField()
    sms_status=models.BooleanField()
    mail_status=models.BooleanField()
    whatsapp_status=models.BooleanField()
    executed_on=models.DateTimeField(null=True)
    sms_id=models.CharField(max_length=100,null=True)
    mail_id=models.CharField(max_length=100,null=True)
    whatsapp_id=models.CharField(max_length=100,null=True)
   

def image_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_images.{}'.format(instance.user, ext)
    else:
        filename = '{}_images.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

def video_rename(instance, filename):
    upload_to = 'videos'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_video.{}'.format(instance.user, ext)
    else:
        filename = '{}_video.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

def audio_rename(instance, filename):
    upload_to = 'audios'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_audio.{}'.format(instance.user, ext)
    else:
        filename = '{}_audio.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

def document_rename(instance, filename):
    upload_to = 'documents'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_document.{}'.format(instance.user, ext)
    else:
        filename = '{}_document.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)



class information(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    message=models.TextField(null=True)
    images=models.FileField(upload_to=image_rename,null=True)
    videos=models.FileField(upload_to=video_rename,null=True)
    audios=models.FileField(upload_to=audio_rename,null=True)
    documents=models.FileField(upload_to=document_rename,null=True)


class Jobs(models.Model):
   job_name = models.CharField(max_length=100)
   next_run_time = models.DateTimeField(null=True, blank=True)
   def __str__(self):
       return self.job_name

class JobExecution(models.Model):
   job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
   runtime = models.DateTimeField(auto_now_add=True)
   error = models.TextField(null=True, blank=True)
   status = models.CharField(max_length=100)
   def __str__(self):
       return f"{self.job} - {self.runtime}"

@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)
            

@receiver(pre_save)
def delete_files_when_file_changed(sender,instance, **kwargs):
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                return
            instance_in_db_file_field = getattr(instance_in_db,field.name)
            instance_file_field = getattr(instance,field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

 
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)