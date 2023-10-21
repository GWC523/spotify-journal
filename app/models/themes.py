from . import db

class Themes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    primary_color = db.Column(db.String(50), nullable=False)
    secondary_color = db.Column(db.String(50), nullable=False)
    tertiary_color = db.Column(db.String(50), nullable=False)
    font_family = db.Column(db.String(100), nullable=False)
    background_image_url = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, primary_color, secondary_color, tertiary_color, font_family, background_image_url, description):
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.tertiary_color = tertiary_color
        self.font_family = font_family
        self.background_image_url = background_image_url
        self.description = description

    def __repr__(self):
        return f'<Theme {self.name}>'
