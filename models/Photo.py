from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class PhotoModel(db.Model):
    __tablename__ = 'photo_model'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())