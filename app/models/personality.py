from . import db

class Personality(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, title, description=None):
        self.title = title
        self.description = description

    def __repr__(self):
        return f'<Personality {self.id}>'




