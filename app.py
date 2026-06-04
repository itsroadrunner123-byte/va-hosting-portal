from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

# Import db and models from models.py
from models import db, User, Package, ServerConfig, Ticket

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

@app.route('/')
def index():
    # Basic check if DB is accessible
    db_status = "Unknown"
    try:
        with app.app_context(): # Ensure it's within app context for db operations
            db.session.execute(db.text('SELECT 1'))
            db_status = "Connected"
    except Exception as e:
        db_status = f"Error: {e}"
        # In a real app, you'd log this error properly
    return render_template('index.html', db_status=db_status)

# Example route for user registration (will be fleshed out)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password') # Needs hashing!

        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('register'))

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))

        # TODO: Hash the password before storing
        # In production, use werkzeug.security.generate_password_hash
        new_user = User(username=username, email=email, password_hash="hashed_password_placeholder")
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {e}', 'danger')
            return redirect(url_for('register'))

    return render_template('auth/register.html')

# Example route for login (will be fleshed out)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        # TODO: Check password hash securely here
        if user and password == "correct_password_placeholder": # Placeholder for password check
            flash('Login successful!', 'success')
            # TODO: Implement session management
            return redirect(url_for('index')) # Redirect to dashboard or index
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html')

# Placeholder for file upload route
@app.route('/upload_beacon', methods=['POST'])
def upload_beacon():
    # TODO: Implement actual file saving and association with ServerConfig
    if 'beacon_file' not in request.files:
        flash('No file part in the form', 'danger')
        return redirect(url_for('index')) # Redirect to a relevant page
    file = request.files['beacon_file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('index'))
    
    if file:
        # In production, save file securely to a defined location (e.g., cloud storage or Render's filesystem)
        # For now, we'll just indicate success. Actual saving mechanism needs to be implemented.
        filename = file.filename # Basic filename
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Example of saving
        flash(f'File "{filename}" received. Processing logic to be implemented.', 'info')
        return redirect(url_for('index')) # Or a confirmation page
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        # This block is for local development to create tables if they don't exist.
        # On Render, you'll use migrations or Render's database tools.
        db.create_all()
    app.run(debug=True) # Set debug=False for production
