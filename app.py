from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# HTML Templates as Strings
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>CRUD App</title>
</head>
<body>
    <h1>User List</h1>
    <a href="/add">Add New User</a>
    <ul>
    {% for user in users %}
        <li>
            {{ user[1] }} ({{ user[2] }})
            <a href="/edit/{{ user[0] }}">Edit</a>
            <a href="/delete/{{ user[0] }}">Delete</a>
        </li>
    {% endfor %}
    </ul>
</body>
</html>
"""

add_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Add User</title>
</head>
<body>
    <h1>Add User</h1>
    <form method="POST">
        Name: <input type="text" name="name"><br><br>
        Email: <input type="text" name="email"><br><br>
        <input type="submit" value="Add">
    </form>
</body>
</html>
"""

edit_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Edit User</title>
</head>
<body>
    <h1>Edit User</h1>
    <form method="POST">
        Name: <input type="text" name="name" value="{{ user[1] }}"><br><br>
        Email: <input type="text" name="email" value="{{ user[2] }}"><br><br>
        <input type="submit" value="Update">
    </form>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return render_template_string(index_html, users=users)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name,email) VALUES (?,?)", (name,email))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template_string(add_html)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        c.execute("UPDATE users SET name=?, email=? WHERE id=?", (name,email,id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM users WHERE id=?", (id,))
        user = c.fetchone()
        conn.close()
        return render_template_string(edit_html, user=user)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Run app on live server
if __name__ == "__main__":
    init_db()
    app.run(host="192.168.1.3", port=5000, debug=True)

