from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from extensions import db

class User(db.Model):
    __tablename__ = 'users'
   
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    accounts = relationship("Account", back_populates="user")