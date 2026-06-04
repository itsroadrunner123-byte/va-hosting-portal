from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a_default_secret_key_for_dev') # Use a strong key in production

# Database configuration
# Render will provide DATABASE_URL in environment variables.
# For local development, you'll set this in your .env file.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Placeholder for your database models (we'll define these later)
# from models import User, Package, Ticket, ServerConfig # Example import

@app.route('/')
def index():
    # Render homepage template
    return render_template('index.html')

# Example route for user registration (will be fleshed out)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html')

# Example route for login (will be fleshed out)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data
        flash('Login successful!', 'success')
        return redirect(url_for('index')) # Redirect to dashboard or index
    return render_template('auth/login.html')

# Placeholder for file upload route
@app.route('/upload_beacon', methods=['POST'])
def upload_beacon():
    # Handle Beacon file upload
    if 'beacon_file' not in request.files:
        flash('No file part in the form', 'danger')
        return redirect(request.url)
    file = request.files['beacon_file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    if file:
        # Save the file or process it
        filename = file.filename # In production save securely to a defined location
        file.save(filename) # Placeholder: implement secure saving logic
        flash(f'File {filename} uploaded successfully!', 'success')
        return redirect(url_for('index')) # Or wherever appropriate
    return redirect(url_for('index'))


if __name__ == '__main__':
    # For local development: create tables if they don't exist
    # In production on Render, migrations or direct table creation via DB tools is preferred
    with app.app_context():
        # db.create_all() # Uncomment when models are defined
        pass
    app.run(debug=True) # Set debug=False for production
