from flask import Flask, render_template,make_response,request
import time
import requests
import re
import base64

app = Flask(__name__)


def getenc_int_sessionid():
    sess = requests.Session()
    headers = {
        # auto delete br encoding. cos requests and scrapy can not decode it.
        # "accept-encoding": "gzip, deflate",
        "accept-language": "zh-CN,zh;q=0.9",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "user-agent": "yuanrenxue.project"
    }
    sess.headers.update(headers)

    # 设置sessionid
    response1 = sess.get('http://match.yuanrenxue.com/match/10')
    search_sessionid = re.search('sessionid=(.*?); ', response1.headers['Set-Cookie'])
    if search_sessionid:
        sessionid = search_sessionid.group(1)
    # print('sessionid', sessionid)
    enc_int = int(re.findall(r'yuanrenxue_59 *= *(\d+)', response1.text)[0])
    # print('enc_int', enc_int)
    return enc_int,sessionid


def getEvalsrt(value1,value2,value3,offset):
    with open('eval-c2.js','r',encoding='utf-8') as f:
        raw_text = f.read()
        temp = re.sub(r"{{value1}}",value1,raw_text,re.S)
        temp = re.sub(r"{{value2}}",value2,temp,re.S)
        temp = re.sub(r"{{value3}}",value3,temp,re.S)
        return re.sub(r"{{offset}}",offset,temp,re.S)


@app.route("/")
def index():
    pagetitle = "HomePage"
    ts = str(int(time.time()*1000))
    return render_template("index.html",
                           mytitle=pagetitle,
                           mycontent="Hello World render_template" + ts)

@app.route("/10")
def yuanrenxue():
    enc_int ,sessionid = getenc_int_sessionid()
    resp = make_response(render_template("10.html",title='skygongque',enc_int=enc_int))
    resp.set_cookie('sessionid',sessionid)
    return resp


@app.route('/eval')
def evalstr():
    """ http://127.0.0.1:5000/eval?value1=1&value2=2&value3=3&offset=abcv """
    value1 = request.args.get('value1')
    value2 = request.args.get('value2')
    value3 = request.args.get('value3')
    offset = request.args.get('offset')
    print(value1,value2,value3,offset)
    if value1 and value2 and value3 and offset:
        return getEvalsrt(value1,value2,value3,offset)
    else:
        return 'no params'


if __name__ == "__main__":
    app.run(debug=True)
