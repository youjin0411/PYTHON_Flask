from datetime import date
from flask import Flask, render_template, request
import random
from csv import excel
from operator import index, indexOf
# 랜덤 아이디 생성하기
from random import Random
import pandas as pd
# 엑셀 파일 읽기
from pandas import read_excel
# 엑셀 파일 읽기

data = pd.read_excel('db.xlsx')
li = []
passli = []

data2 = pd.read_excel('idname.xlsx')
li2 = []
passli2 = []

app = Flask(__name__)

# 시작 index.html
@app.route("/")
def hello():
    return render_template('index.html')
# 아이디 생성 선택 - 일반/인스타 선택
@app.route('/choi')
def choi():
    return render_template('choi.html')

# 일반 아이디 생성 페이지
@app.route('/randId')
def randId():
    return render_template('randId.html')

# 일반 아이디 생성 결과 페이지
@app.route('/randIdres', methods = ['POST', 'GET'])
def randIdres():
    if request.method == 'POST':
        id =  request.form.getlist('id[]')
        # 엑셀 파일의 숫자 암호 리스트li에 담기
        for i in range(len(data['암호'])):
            li.append(data['암호'][i])

        # 엑셀 파일의 암호 의미 리스트 passli에 담기
        for i in range(len(data['의미'])):
            passli.append(data['의미'][i])

        # 리스트 li안에 있는 숫자 암호 랜덤으로 하나 makeId에 주기
        makeId = random.sample(li, 1)
        ind = li.index(makeId)

        # [] 빠져나오기
        id = str(id).strip('[]')
        id = str(id).strip("''")
        makeId = str(makeId).strip('[]')
        id_mean = str(passli[ind]).strip('[]')
        return render_template('randIdres.html', date=makeId, date2=id_mean, id=id)

# 아이디 생성 페이지
@app.route('/randinsId')
def randinsId():
    return render_template('randinsId.html')

# 인스타 아이디 생성 결과 페이지
@app.route('/randinsIdres', methods = ['POST', 'GET'])
def randinsIdres():
    if request.method == 'POST':
        id =  request.form.getlist('id[]')
    # 엑셀 파일의 인스타 아이디 리스트li2에 담기
        for i in range(len(data2['아이디'])):
            li2.append(data2['아이디'][i])	
    # 엑셀 파일의 암호 의미 리스트 passli2에 담기
        for i in range(len(data2['의미'])):
            passli2.append(data2['의미'][i])
    # 리스트 li2안에 있는 숫자 암호 랜덤으로 하나 makeId2에 주기
        makeId2 = random.sample(li2, 1)
        ansId = ' '.join(map(str, makeId2))
        ind2 = li2.index(ansId)
    # [] 빠져나오기
        id = str(id).strip('[]')
        id = str(id).strip("''")
        makeId2 = str(makeId2).strip('[]')
        makeId2 = str(makeId2).strip("''")
        id_mean2 = str(passli2[ind2]).strip('[]')
        return render_template('randinsIdres.html', date=makeId2, date2=id_mean2, id=id)

# 아이디 의미 확인 페이지
@app.route('/idmean')
def idmean():
    return render_template('idmean.html')

# 일반 아이디 의미 확인 페이지
@app.route('/meandateid')
def meandateid():
    return render_template('meandateid.html',data=data)

# 인스타 아이디 의미 확인 페이지
@app.route('/meandateinsid')
def meandateinsid():
    return render_template('meandateinsid.html', data2=data2)

if __name__ == "__main__":
    app.run()
