from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

# 테스트 시작하기
@app.route('/randId')
def start():
    return render_template('randId.html')

@app.route('/randIdres')
def start2():
    return render_template('randIdres.html')

if __name__ == "__main__":
    app.run()
