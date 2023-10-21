from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False)
    theme_id = db.Column(db.Integer, ForeignKey('theme.id'), nullable=True)
    mood_id = db.Column(db.Integer, ForeignKey('mood.id'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    track_id = db.Column(db.String(50), nullable=True)
    added_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_on = db.Column(db.DateTime, default=None, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    user = relationship('User', backref='entries')
    theme = relationship('Theme', backref='entries')
    mood = relationship('Mood', backref='entries')

