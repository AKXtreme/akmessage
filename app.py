import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, emit
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, ChatRoom, Message, Conversation

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///akmessage.db'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'webm'}

db.init_app(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)
migrate = Migrate(app, db)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

@app.context_processor
def utility_processor():
    def user_by_id(user_id):
        return User.query.get(user_id)
    return dict(user_by_id=user_by_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('conversations'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/conversations')
@login_required
def conversations():
    user_conversations = current_user.conversations
    return render_template('conversations.html', conversations=user_conversations)

@app.route('/conversation/<int:conv_id>', methods=['GET', 'POST'])
@login_required
def conversation(conv_id):
    conv = Conversation.query.get_or_404(conv_id)
    if request.method == 'POST':
        msg = request.form.get('msg')
        file = request.files.get('file')
        voice = request.files.get('voice')
        file_path = None

        # Handle file upload
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        # Handle voice upload
        if voice and voice.filename and allowed_file(voice.filename):
            voice_filename = secure_filename(voice.filename)
            voice_path = os.path.join(app.config['UPLOAD_FOLDER'], voice_filename)
            voice.save(voice_path)
            file_path = voice_path  # Prefer voice if both are present

        message = Message(
            content=msg,
            user_id=current_user.id,
            conversation_id=conv.id,
            file_path=file_path
        )
        db.session.add(message)
        db.session.commit()
    messages = Message.query.filter_by(conversation_id=conv.id).order_by(Message.timestamp).all()
    return render_template('conversation.html', conversation=conv, messages=messages)

@app.route('/start_conversation', methods=['GET', 'POST'])
@login_required
def start_conversation():
    users = User.query.filter(User.id != current_user.id).all()
    if request.method == 'POST':
        user_ids = request.form.getlist('user_ids')
        is_group = len(user_ids) > 1
        conv = Conversation(is_group=is_group)
        conv.users.append(current_user)
        for uid in user_ids:
            user = User.query.get(int(uid))
            if user:
                conv.users.append(user)
        if is_group:
            conv.name = request.form.get('group_name') or "Group Chat"
        db.session.add(conv)
        db.session.commit()
        return redirect(url_for('conversation', conv_id=conv.id))
    return render_template('start_conversation.html', users=users)

# --- SocketIO events for real-time chat ---
@socketio.on('join')
def handle_join(data):
    room = str(data['room'])
    join_room(room)

@socketio.on('send_message')
def handle_send_message(data):
    room = str(data['room'])
    msg = data['msg']
    message = Message(content=msg, user_id=current_user.id, conversation_id=int(room))
    db.session.add(message)
    db.session.commit()
    emit('receive_message', {
        'user': current_user.username,
        'msg': msg
    }, room=room)
# Duplicate conversation route removed to avoid Flask routing error.
if __name__ == '__main__':
    socketio.run(app, debug=True)