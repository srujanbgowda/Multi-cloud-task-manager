from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create database table
def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

# Homepage - View tasks
@app.route('/')
def home():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add task
@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']

    if title.strip():
        conn = get_db()
        conn.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        conn.commit()
        conn.close()

    return redirect('/')

# Update task status
@app.route('/complete/<int:id>')
def complete_task(id):
    conn = get_db()
    conn.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect('/')

# Delete task
@app.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

# Edit task
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):

    conn = get_db()

    if request.method == 'POST':
        title = request.form['title']

        conn.execute(
            "UPDATE tasks SET title = ? WHERE id = ?",
            (title, id)
        )

        conn.commit()
        conn.close()

        return redirect('/')

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (id,)
    ).fetchone()

    conn.close()

    return render_template('edit.html', task=task)

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
