from flask import Flask, render_template, jsonify, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'supersecretkey'  # 보안 키
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


# 데이터베이스, 암호화, 로그인 관리 설정
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# 사용자 모델 정의
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# DB 테이블 생성 (앱 실행 시 한 번만 실행)
with app.app_context():
    db.create_all()

# 로봇 상태 (활성화/비활성화) 관리 변수
robot_active = True

# 홈 라우트
@app.route('/')
def home():
    return render_template('index.html')

# 회원가입 라우트
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('이미 존재하는 사용자입니다.', 'danger')
            return redirect(url_for('register'))

        # 비밀번호 암호화 후 저장
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입 성공! 로그인하세요.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# 대시보드 라우트
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# 로그인 라우트
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('로그인 성공!', 'success')
            return redirect(url_for('dashboard'))  # 대시보드로 리디렉션
        else:
            flash('로그인 실패. 아이디 또는 비밀번호를 확인하세요.', 'danger')
            return redirect(url_for('login'))  # 로그인 페이지로 리디렉션

    return render_template('login.html')  # GET 요청 시 로그인 페이지 렌더링

# QR 코드 페이지 라우트
@app.route('/qr_code')
def qr_code():
    return render_template('qr_code.html')

# 문제 신고 페이지 라우트
@app.route('/report_issue')
def report_issue():
    return render_template('report_issue.html')

# 스트리밍 및 경찰 신고 페이지 라우트
@app.route('/streaming_and_report')
@login_required
def streaming_and_report():
    return render_template('streaming_and_report.html')

# 로그아웃
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 되었습니다.', 'info')
    return redirect(url_for('login'))

# 로봇 위치 API (JSON 응답)
@app.route('/robot_location')
def robot_location():  
    return render_template('robot_location.html')

# 로봇 비활성화 페이지 라우트
@app.route('/disable_robot', methods=['GET', 'POST'])
@login_required
def disable_robot():
    global robot_active
    if request.method == 'POST':
        # 버튼을 클릭하면 로봇을 비활성화
        robot_active = False
        flash('로봇이 비활성화되었습니다.', 'info')
        return redirect(url_for('dashboard'))  # 대시보드로 리디렉션

    # 로봇 활성화 상태 확인 후 페이지 렌더링
    return render_template('disable_robot.html', robot_active=robot_active)

if __name__ == '__main__':
    app.run(debug=True)
