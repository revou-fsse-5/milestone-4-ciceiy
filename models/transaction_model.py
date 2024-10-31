from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from extensions import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
   
    id = db.Column(db.Integer, primary_key=True, index=True)
    from_account_id = db.Column(db.Integer, ForeignKey('accounts.id'))
    to_account_id = db.Column(db.Integer, ForeignKey('accounts.id'))
    amount = db.Column(db.Numeric(10, 2))
    type = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="transactions_from")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="transactions_to")