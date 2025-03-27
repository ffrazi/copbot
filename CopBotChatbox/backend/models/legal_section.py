from backend.models.database import db

class LegalSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<LegalSection {self.section_name}>'
