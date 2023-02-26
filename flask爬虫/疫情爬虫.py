import requests
import json
json_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0'
    ,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.41'
}
resp=requests.get(json_url,headers=header)
json_data=resp.text
print(json_data)
d_data=json.loads(json_data)
print(d_data)
data_history=json.loads(d_data['data'])
for i in data_history.keys():
    print(i)
    print(data_history[i])