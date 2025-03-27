from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import geocoder

app = Flask(__name__)
app.secret_key = "supersecretkey"  # 세션을 위한 키

# 임시 사용자 정보 (데이터베이스 대신 사용)
USER_ID = "admin"
USER_PW = "password"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 아이디와 비밀번호가 올바른지 확인
        if username == USER_ID and password == USER_PW:
            session['user'] = username
            return redirect(url_for('index'))  # 로그인 후 메인 페이지로 리디렉션
        else:
            return "아이디 또는 비밀번호가 틀립니다."  # 로그인 실패 메시지
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # 'user'로 session에서 값을 제거
    return redirect(url_for('index'))

@app.route('/get_user')
def get_user():
    user = session.get('user')  # session.get()을 사용하여 안전하게 값 조회
    if user:
        return jsonify({'logged_in': True, 'username': user})
    else:
        return jsonify({'logged_in': False})
    
@app.route('/scan')
def scan():
    return render_template('scan.html')


if __name__ == '__main__':
    app.run(debug=True)
