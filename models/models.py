# This file is now the models.py inside the models directory.
# Its content remains the same as previously defined.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Store hashed passwords!
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_monthly = db.Column(db.Float, nullable=False)
    player_slots = db.Column(db.Integer, nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    cpu_cores = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Package {self.name}>'

class ServerConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False)
    beacon_file_path = db.Column(db.String(255), nullable=True)
    server_ip = db.Column(db.String(100), nullable=True)
    rcon_password = db.Column(db.String(100), nullable=True)
    provisioning_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('server_configs', lazy=True))
    package = db.relationship('Package', backref=db.backref('server_configs', lazy=True))

    def __repr__(self):
        return f'<ServerConfig {self.id} for User {self.user_id}>'

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

    def __repr__(self):
        return f'<Ticket {self.id} - {self.subject}>'