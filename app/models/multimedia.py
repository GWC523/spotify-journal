from . import db

class Multimedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)

    def __init__(self, user_id, entry_id):
        self.user_id = user_id
        self.entry_id = entry_id

    def __repr__(self):
        return f'<Multimedia {self.id}>'
