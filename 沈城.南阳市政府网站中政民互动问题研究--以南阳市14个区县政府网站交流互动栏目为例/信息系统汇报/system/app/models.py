from django.db import models

# Create your models here.
class consultdata(models.Model):
    id=models.IntegerField(primary_key=True,default=0)
    consultCategory=models.CharField(max_length=4,default='')
    consultTitle=models.CharField(max_length=50,default='')
    consultName=models.CharField(max_length=50,default='')
    consultDate=models.CharField(max_length=50,default='')
    consultId=models.CharField(max_length=50,default='')
    consultDepartment=models.CharField(max_length=50,default='')
    consultState=models.CharField(max_length=50,default='')
    consultContent=models.TextField(blank=True,default='')
    answerDepartment=models.CharField(max_length=50,default='')
    answerDate=models.CharField(max_length=50,default='')
    answerContent=models.TextField(blank=True,default='')