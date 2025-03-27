from .database import db

class Query(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Query {self.question}>'
