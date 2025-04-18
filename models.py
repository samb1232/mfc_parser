from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Ticket(db.Model):
    id = db.Column(db.String, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
