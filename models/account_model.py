from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from extensions import db

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True, index=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    account_type = db.Column(db.String(255))
    account_number = db.Column(db.String(255), unique=True)
    balance = db.Column(db.Numeric(10, 2), default=0.0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="accounts")
    
    transactions_from = relationship("Transaction", foreign_keys='Transaction.from_account_id', back_populates="from_account")
    transactions_to = relationship("Transaction", foreign_keys='Transaction.to_account_id', back_populates="to_account")