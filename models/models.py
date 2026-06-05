from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) # Store hashed passwords!
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships can be added later, e.g., relation to ServerConfig, Tickets

    def __repr__(self):
        return f'<User {self.username}>'

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_monthly = db.Column(db.Float, nullable=True) # Nullable as prices will be provided later
    player_slots = db.Column(db.Integer, nullable=False)
    ram_gb = db.Column(db.Integer, nullable=True, default=8) # Placeholder default RAM
    cpu_cores = db.Column(db.Integer, nullable=True, default=4) # Placeholder default CPU

    # Note on subscription periods: For now, packages are named with their duration in mind (e.g., "20 Player Slots - 1 Month").
    # Actual pricing logic for different durations will be handled in the application code or a separate plan model.

    def __repr__(self):
        return f'<Package {self.name}>'

class ServerConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    package_id = db.Column(db.Integer, db.ForeignKey('package.id'), nullable=False) # Links to Package
    beacon_file_path = db.Column(db.String(255), nullable=True) # Path to uploaded Beacon export file
    map_save_file_path = db.Column(db.String(255), nullable=True) # Path to uploaded Map save file
    server_ip = db.Column(db.String(100), nullable=True) # Assigned IP address IF applicable
    rcon_password = db.Column(db.String(100), nullable=True) # Or store securely elsewhere
    provisioning_status = db.Column(db.String(50), default='pending') # e.g., pending, provisioning, active, failed
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
    status = db.Column(db.String(50), default='open') # e.g., open, in_progress, resolved, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Optional: server_config_id = db.Column(db.Integer, db.ForeignKey('server_config.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('tickets', lazy=True))

    def __repr__(self):
        return f'<Ticket {self.id} - {self.subject}>'
