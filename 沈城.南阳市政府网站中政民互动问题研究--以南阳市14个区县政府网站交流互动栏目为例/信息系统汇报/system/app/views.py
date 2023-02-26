from django.shortcuts import render
from django.views.generic import View
from .models import consultdata
import pandas as pd
import json
import numpy as np
import json
# Create your views here.
class consult(View):
    def get(self,request):
        data = pd.read_excel("/home/sc/桌面/信息系统汇报/system/static/hd.xlsx")
        if str(consultdata.objects.all())== '<QuerySet []>':
            for i in range(1,len(data)+1):
                consultdata.objects.create(id=i,consultCategory=data['consultCategory'][i-1],consultTitle=data['consultTitle'][i-1],consultName=data['consultName'][i-1],consultId=str(data['consultId'][i-1]),consultDate=data['consultDate'][i-1],consultDepartment=data['consultDepartment'][i-1],consultState=data['consultState'][i-1],consultContent=data['consultContent'][i-1],answerDepartment=data['answerDepartment'][i-1],answerDate=data['answerDate'][i-1],answerContent=data['answerContent'][i-1])
            info1=consultdata.objects.all().values('id')
        else:
            for i in range(len(data)):
                consultdata.objects.filter(id=f'{i}').update(consultCategory=data['consultCategory'][i],consultTitle=data['consultTitle'][i],consultName=data['consultName'][i],consultId=str(data['consultId'][i]),consultDate=data['consultDate'][i],consultDepartment=data['consultDepartment'][i],consultState=data['consultState'][i],consultContent=data['consultContent'][i],answerDepartment=data['answerDepartment'][i],answerDate=data['answerDate'][i],answerContent=data['answerContent'][i])
            Id=np.array(consultdata.objects.all().values('id')).tolist()
            consultCategory=np.array(consultdata.objects.all().values('consultCategory')).tolist()
            consultTitle=np.array(consultdata.objects.all().values('consultTitle')).tolist()
            consultName=np.array(consultdata.objects.all().values('consultName')).tolist()
            consultId=np.array(consultdata.objects.all().values('consultId')).tolist()
            consultDate=np.array(consultdata.objects.all().values('consultDate')).tolist()
            consultDepartment=np.array(consultdata.objects.all().values('consultDepartment')).tolist()
            consultState=np.array(consultdata.objects.all().values('consultState')).tolist()
            consultContent=np.array(consultdata.objects.all().values('consultContent')).tolist()
            answerDepartment=np.array(consultdata.objects.all().values('answerDepartment')).tolist()
            answerDate=np.array(consultdata.objects.all().values('answerDate')).tolist()
            answerContent=np.array(consultdata.objects.all().values('answerContent')).tolist()
        return render(request,'index.html',{'dataLength':json.dumps(len(data)),'Id':json.dumps(Id),'consultCategory':json.dumps(consultCategory),'consultTitle':json.dumps(consultTitle),'consultName':json.dumps(consultName),'consultId':json.dumps(consultId),'consultDate':json.dumps(consultDate),'consultDepartment':json.dumps(consultDepartment),'consultState':json.dumps(consultState),'consultContent':json.dumps(consultContent),'answerDepartment':json.dumps(answerDepartment),'answerDate':json.dumps(answerDate),'answerContent':json.dumps(answerContent)})