from datetime import date
from flask import Flask, session, render_template, redirect, request, url_for
from flask import flash
from flaskext.mysql import MySQL
import MySQLdb.cursors
import re
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

mysql = MySQL()
app = Flask(__name__)
app.config["SECRET_KEY"] = "ABCD"

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'  
app.config['MYSQL_DATABASE_DB'] = 'login'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.secret_key = "1234"
mysql.init_app(app)

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
    data = pd.read_excel('db.xlsx')
    li = []
    passli = []
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

        error = None
        user = session['id']
        conn = mysql.connect()
        cursor = conn.cursor()

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO save_id (user, saveid, savemean) VALUES (%s, %s, %s)"
        saveid = id,"_",makeId
        saveid = "".join(saveid)
        value = (user, saveid, id_mean)
        cursor.execute(sql, value)

        d = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('randIdres.html',date=makeId, date2=id_mean, id=id)

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

        error = None
        user = session['id']
        conn = mysql.connect()
        cursor = conn.cursor()

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO save_id (user, saveid, savemean) VALUES (%s, %s, %s)"
        saveid = id,"_",makeId2
        saveid = "".join(saveid)
        value = (user, saveid, id_mean2)
        cursor.execute(sql, value)

        d = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()
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

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def main():
    error = None
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        name = request.form['name']
 
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM mypage WHERE id = %s AND password = %s AND name = %s"
        value = (id, pw, name)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
 
        data = cursor.fetchall()
             
        for row in data:
            data = row[0]

        cursor.close()
        conn.close()
        if data:
            session['login'] = name
            session['id'] = id
            session['pw'] = pw 
            return redirect(url_for('mypage')) 
        else:
            flash('아이디 또는 비밀번호가 틀렸습니다.')
            return render_template('login.html')
    return render_template('login.html', error = error)

# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        id = request.form['regi_id']
        pw = request.form['regi_pw']
        name = request.form['regi_name']
        animal = request.form['result']

        conn = mysql.connect()
        cursor = conn.cursor()

        sql = "SELECT * FROM mypage WHERE id = %s AND password = %s"
        value = (id, pw)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
 
        data = cursor.fetchall()
 
        for row in data:
            data = row[0]

        if id == "" or pw == "" or name == "":
            flash("아이디와 비밀번호, 이름을 입력해주세요.")
            return render_template("signup.html")
        elif animal == "":
            flash("동물을 선택해주세요.")
            return render_template("signup.html")
 
        if not data and id != "" and pw != "":
            sql = "INSERT INTO mypage (id, password, name, ans) VALUES(%s, %s, %s, %s)"
            value = (id, pw, name, animal)
            cursor.execute("set names utf8")
            cursor.execute(sql, value)
    
            data = cursor.fetchall()

            if not data:
                conn.commit()
                return redirect('/login')
            else:
                conn.rollback()
                flash("중복된 이메일 주소입니다.")
                return render_template("signup.html")
            
        cursor.close()
        conn.close()
        flash("중복된 이메일 주소입니다.")
    return render_template('signup.html', error=error)

# 마이페이지
@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if 'login' not in session:
        return render_template('login.html')
    error = None
    name = session['login']
    id = session['id']
    pw = session['pw']
    char = ''
    money = ''

    conn = mysql.connect()
    cursor = conn.cursor()
    sql2 = "SELECT * FROM mypage WHERE id = %s"
    value2 = (id)
    cursor.execute("set names utf8")
    cursor.execute(sql2, value2)
    data = cursor.fetchall()
    for row in data:
        char = row[5]
        money = row[4]
    # data에서 ans값만 뽑아내기
    cursor.close()
    conn.close()

    if money == None:
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "update mypage set money = %s where id = %s"
        value = (0,id)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
        conn.commit()
        cursor.close()
        conn.close()

    conn = mysql.connect()
    cursor = conn.cursor()
    sql2 = "SELECT * FROM mypage WHERE id = %s"
    value2 = (id)
    cursor.execute("set names utf8")
    cursor.execute(sql2, value2)
    data = cursor.fetchall()
    for row in data:
        money = row[4]
    # data에서 ans값만 뽑아내기
    cursor.close()
    conn.close()

    if request.method == 'POST':
        if money < 200 or money == 0 or money == None:
            flash("돈이 부족합니다.")
            return render_template('store.html', money = money)
        else:
            char = request.form['cute']  
            money = money - 200
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = "update mypage set ans = %s, money = %s where id = %s"
            value = (char ,money, id)
            cursor.execute("set names utf8")
            cursor.execute(sql, value)
            conn.commit()
            cursor.close()
            conn.close()
    return render_template('mypage.html', error=error, name=name, id=id, pw=pw, char=char, money=money)

@app.route('/saveidview', methods=['GET', 'POST'])
def saveidview():
    error = None
    id = session['id']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM save_id WHERE user = %s"
    value = (id)
    cursor.execute("set names utf8")
    cursor.execute(sql, value)
    data = cursor.fetchall()
    # data에서 ans값만 뽑아내기

    result = []
    result2 = []
    for row in data:
        result.append(row[2])

    for row2 in data:
        result2.append(row2[3])

    cursor.close()
    conn.close()

    return render_template('saveidview.html', error=error, char=result, char2 = result2)


@app.route('/makeid', methods=['GET', 'POST'])
def makeid():
    return render_template('makeid.html')

@app.route('/makeidres', methods=['GET', 'POST'])
def makeidres():
    if request.method == 'POST':
        id = request.form['name[]']
        pw = request.form['pw[]']
        mean = request.form['mean[]']

        id = str(id).strip('[]')
        id = str(id).strip("''")

        error = None
        user = session['id']
        conn = mysql.connect()
        cursor = conn.cursor()

        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "INSERT INTO save_id (user, saveid, savemean) VALUES (%s, %s, %s)"
        saveid = id,"_",pw
        saveid = "".join(saveid)
        value = (user, saveid, mean)
        cursor.execute(sql, value)

        d = cursor.fetchall()
        
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('makeidres.html', id=id, data=pw, data2=mean)

@app.route('/game', methods=['GET', 'POST'])
def game():
        global data
        lis = []
        passlis = []

        # 엑셀 파일의 숫자 암호 리스트li에 담기
        for i in range(len(data['암호'])):
            lis.append(data['암호'][i])

        # 엑셀 파일의 암호 의미 리스트 passli에 담기
        for i in range(len(data['의미'])):
            passlis.append(data['의미'][i])

        # 리스트 li안에 있는 숫자 암호 랜덤으로 하나 makeId에 주기
        makeId = random.sample(lis, 1)
        ind = lis.index(makeId)

        # [] 빠져나오기
        makeId = str(makeId).strip('[]')
        id_mean = str(passlis[ind]).strip('[]')

        error = None
        id = session['id']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM mypage WHERE id = %s"
        value = (id)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
        data = cursor.fetchall()
        for row in data:
            data = row[4]
        cursor.close()
        conn.close()

        data = data + 100
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "update mypage set money = %s where id = %s"
        value = (data,id)
        cursor.execute("set names utf8")
        cursor.execute(sql, value)
        conn.commit()
        cursor.close()
        conn.close()
        return render_template('game.html', makeId=makeId, id_mean=id_mean, money=data)

@app.route('/store', methods=['GET', 'POST'])
def store():
    id = session['id']
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = "SELECT * FROM mypage WHERE id = %s"
    value = (id)
    cursor.execute("set names utf8")
    cursor.execute(sql, value)
    data = cursor.fetchall()
    for row in data:
        data = row[4]
    cursor.close()
    conn.close()
    money = data
    return render_template('store.html', money=money)

if __name__ == "__main__":
    app.run()