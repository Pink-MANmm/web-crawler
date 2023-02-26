import requests
import xlwt


url = 'http://119.29.79.190:7702/fstmicd/js/ExternalWebSite/config.json?v=1663462833304/data/纺织服装个股资金流.json'
data_dict = requests.get(url).json()
# 筛选条件
cp_type = ['坯布','成衣','资料','棉纱']
dq_type = ['境内','境外']
show_list = []
for data in data_dict:
    if cp_type and dq_type:
        for i in range(len(cp_type)):
            for j in range(len(data['产品类别'])):
                if data['产品类别'][j].find(cp_type[i]) == -1:
                    continue
                for z in range(len(dq_type)):
                    for k in range(len(data['地区分类'])):
                        if data['地区分类'][k].find(dq_type[z]) == -1:
                            continue
                        if data in show_list:
                            continue
                        show_list.append(data)
# print(data)
    elif len(cp_type) == 0 and len(dq_type) > 0:
        for z in range(len(dq_type)):
            for k in range(len(data['地区分类'])):
                if data['地区分类'][k].find(dq_type[z]) == -1:
                    continue
                if data in show_list:
                    continue
                show_list.append(data)
# print(data)
    elif len(cp_type) > 0 and len(dq_type) == 0:
        for z in range(len(cp_type)):
            for k in range(len(data['产品类别'])):
                if data['产品类别'][k].find(cp_type[z]) == -1:
                    continue
                if data in show_list:
                    continue
                show_list.append(data)
# print(data)
    else:
        show_list = data_dict
        break
print(len(show_list))
save_list = []
ty_list = ['代号', '名称', '营业总收入(元)', '毛利率(%)', '存货周转天数(天)','资产负债率(%)']
for name in show_list:
    new_url = 'http://119.29.79.190:7702/fstmicd/js/ExternalWebSite/config.json?v=1663462833304/data/主要指标/{}.json'.format(name['名称'])
    data_new = requests.get(new_url).json()
    data = data_new['主要指标']['年度']['数据']
    dd_list = [name['代码'], name['名称']]
    for dd in data:
        if dd["截止日期"] == "2019年12月31日":
            dd_list = dd_list + [dd['营业总收入(元)'], dd['毛利率(%)'], dd['存货周转天数(天)'],dd['资产负债率(%)']]
    save_list.append(dd_list)
# 写入excel
workbook = xlwt.Workbook()
sheet = workbook.add_sheet('data')
l = 0
for ty in ty_list:
    sheet.write(0, l, ty)
    l += 1
n = 1
b = 0
for sa in save_list:
    for s in sa:
        sheet.write(n, b, s)
        b += 1
    n += 1
    b = 0
path = '[UserFolderPath]/data1.xls'
workbook.save(path)
