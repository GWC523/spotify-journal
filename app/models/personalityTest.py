
from . import db

class MusicPersonalityTests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    personality_id = db.Column(db.Integer, db.ForeignKey('personality.id'), nullable=False)
    added_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='music_personality_tests')
    personality = db.relationship('Personality', backref='music_personality_tests')

    def __init__(self, user_id, personality_id):
        self.user_id = user_id
        self.personality_id = personality_id

    def __repr__(self):
        return f'<MusicPersonalityTests {self.id}>'


