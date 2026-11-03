from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'super_secret_key_123'

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS comments (id INTEGER PRIMARY KEY, text TEXT)''')
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT text FROM comments")
    comments = c.fetchall()
    conn.close()
    return render_template('index.html', comments=comments, logged_in='user' in session)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        c.execute(query)
        user = c.fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return "Неверный логин или пароль <br><a href='/login'>Назад</a>"
    return render_template('login.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    text = request.form.get('text', '')
    if text:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO comments (text) VALUES (?)", (text,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/admin')
def admin_panel():
    return "<h1>Секретная админ-панель</h1><p>Флаг: CTF{ADMIN_ACCESS_GRANTED}</p><a href='/'>На главную</a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)