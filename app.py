import os
import uuid
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor, upload_success, upload_fail

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Initialize CKEditor
ckeditor = CKEditor(app)
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'

# Set upload folder and ensure it exists
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

DATABASE = 'portfolio.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Create the projects table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            image TEXT
        )
    ''')
    # Create a new messages table for contact form submissions
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Public Routes

@app.route('/')
def index():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return render_template('index.html', projects=projects)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        subject = request.form.get('subject', '')
        message = request.form['message']
        # Store the message in the database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
            (name, email, subject, message)
        )
        conn.commit()
        conn.close()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/skills')
def skills():
    return render_template('skills.html')

@app.route('/projects')
def projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)

# Admin Routes

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Use secure validation in production
        username = request.form['username']
        password = request.form['password']
        if username == 'aqeel0331' and password == '@Aqeel0317':
            session['logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_file = request.files.get('image')
        image_path = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            image_file.save(filepath)
            # Store relative path (assuming static folder is served)
            image_path = f"uploads/{unique_filename}"
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO projects (title, description, image) VALUES (?, ?, ?)',
            (title, description, image_path)
        )
        conn.commit()
        conn.close()
        flash('Project added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_project.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('dashboard.html', projects=projects, messages=messages)

@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_file = request.files.get('image')
        image_path = project['image']  # keep the old image if no new file is uploaded
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
            image_file.save(filepath)
            image_path = f"uploads/{unique_filename}"
        conn.execute(
            'UPDATE projects SET title = ?, description = ?, image = ? WHERE id = ?',
            (title, description, image_path, id)
        )
        conn.commit()
        conn.close()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    conn.close()
    return render_template('edit_project.html', project=project)

@app.route('/delete_project/<int:id>', methods=['POST'])
def delete_project(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

# CKEditor Image Upload Route

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    if not f:
        return upload_fail('No file uploaded!')
    filename = secure_filename(f.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
    f.save(filepath)
    url = url_for('static', filename='uploads/' + unique_filename)
    return upload_success(url, filename)

@app.route('/project/<int:id>')
def project_detail(id):
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not project:
        flash('Project not found!', 'danger')
        return redirect(url_for('projects'))
    return render_template('project_detail.html', project=project)

if __name__ == '__main__':
    app.run(debug=True)
