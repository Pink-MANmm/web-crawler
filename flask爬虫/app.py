from flask import Flask
from flask import render_template
from jieba.analyse import extract_tags
import util
from flask import jsonify
import string



app = Flask(__name__)


@app.route('/')
def flask():
    return render_template('text.html')

@app.route('/get_sys_time',methods=['get','post'])
def dt():
    dt=util.get()
    return dt

@app.route('/get_center1',methods=['get','post'])
def get_center1():
    res=util.get_center1()
    return jsonify({'confirm':str(res[0]),'suspect':str(res[1]),'heal':str(res[2]),'dead':str(res[3])})

@app.route('/get_center2',methods=['get','post'])
def get_center2():
    datas=[]
    res=util.get_center2()
    for item in res:
        datas.append({'name':item[0],'value':str(item[1])})
    return jsonify({'data':datas})

@app.route('/get_left1',methods=['get','post'])
def get_left1():
    data=util.get_left1()
    day,confirm,suspect,heal,dead=[],[],[],[],[]
    for tup in data:
        day.append(tup[0].strftime('%m-%d'))
        confirm.append(tup[1])
        suspect.append(tup[2])
        heal.append(tup[3])
        dead.append([4])

    return jsonify({'day':day,'confirm':confirm,
                    'suspect':suspect,'heal':heal,
                    'dead':dead})
@app.route('/get_right1',methods=['get','post'])
def get_right1():
    res=util.get_right1()
    city,confirm=[],[]
    for item in res:
        city.append(item[0])
        confirm.append(str(item[1]))
    return jsonify({'city':city,'confirm':confirm})
@app.route('/get_right2',methods=['get','post'])
def get_right2():
    res=util.get_right2()
    content=[]
    for item in res:
        str=item[0].rstrip(string.digits)
        num=item[0][len(str):]
        str=extract_tags(str)
        for data in str:
            if not data.isdigit():
                content.append({'name':data,'value':num})
    print(content)
    return jsonify({'data':content})
@app.route('/get_left2',methods=['get','post'])
def get_left2():
    res=util.get_left2()
    day,confirm_add,suspect=[],[],[]
    for item in res:
        day.append(item[0].strftime('%m-%d'))
        confirm_add.append(item[1])
        suspect.append(item[2])
    return jsonify({'day':day,'confirm_add':confirm_add,'suspect':suspect})

if __name__ == '__main__':
    app.run()