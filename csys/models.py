from django.db import models
from django import forms

# Create your models here.
# class XiaoMai(models.Model):
#     name = '小麦'
#     term = models.CharField(max_length=30)
#     age = models.IntegerField()
#     area = models.CharField(max_length=30)
#     door = models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.name

class Cron(models.Model):
    ctype = models.CharField(max_length=30)
    term = models.CharField(max_length=30)
    year = models.IntegerField()
    area = models.CharField(max_length=30)
    seat = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class UploadFileForm(forms.Form):
    ctype = forms.CharField(max_length=100)
    term = forms.CharField(max_length=100)
    year = forms.CharField(max_length=100)
    area = forms.CharField(max_length=100)
    seat = forms.CharField(max_length=100)
    title = forms.CharField(max_length=100)
    file = forms.FileField()
