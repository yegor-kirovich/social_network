import sqlite3
from data import db_session
from data.user import User
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from flask_login import LoginManager, login_user, current_user

db_session.global_init("database.db")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

login_manager = LoginManager()
login_manager.__init__(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute(f'SELECT * FROM posts WHERE id = {post_id}').fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == request.form.get('email')).first()
        remember = request.form.get('remember')
        if user and user.check_password(request.form.get('password')):
            if remember == "on":
                remember = True
            else:
                remember = False
            login_user(user, remember=remember)
            return redirect('/profile')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db_sess = db_session.create_session()

        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        again_password = request.form.get('again_password')

        if password != again_password:
            flash("Пароль повторен не правильно")
            return render_template('register.html')

        if db_sess.query(User).filter(User.email == email).first():
            flash("Такой пользователь уже есть")
            return render_template('register.html')

        user = User(
            name=name,
            email=email
        )
        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')

    return render_template('register.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template("profile.html", name=current_user.name)


if __name__ == '__main__':
    app.run(debug=1)
