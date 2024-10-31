from flask import Blueprint, request, jsonify
from models.transaction_model import Transaction
from models.account_model import Account
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal

transaction_controller = Blueprint('transaction_controller', __name__)

@transaction_controller.route('/transaction', methods=['POST'])
@jwt_required()
def create_transaction():
    data = request.json
    from_account = Account.query.get(data['from_account_id'])
    to_account = Account.query.get(data['to_account_id'])

    if not from_account or not to_account:
        return {"message": "Account not found"}, 404

    amount = Decimal(data['amount'])

    if from_account.balance < amount:
        return {"message": "Insufficient funds"}, 400

    new_transaction = Transaction(
        from_account_id=data['from_account_id'],
        to_account_id=data['to_account_id'],
        amount=amount,
        type=data['type'],
        description=data.get('description', "")
    )

    from_account.balance -= amount
    to_account.balance += amount

    db.session.add(new_transaction)
    db.session.commit()
    
    return {"message": "Transaction completed"}, 201

@transaction_controller.route('/transaction', methods=['GET'])
@jwt_required()
def get_transactions():
    current_user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    account_ids = [account.id for account in accounts]

    transactions = Transaction.query.filter(
        (Transaction.from_account_id.in_(account_ids)) | 
        (Transaction.to_account_id.in_(account_ids))
    ).all()

    return jsonify([{
        "id": transaction.id,
        "from_account_id": transaction.from_account_id,
        "to_account_id": transaction.to_account_id,
        "amount": float(transaction.amount),
        "type": transaction.type,
        "description": transaction.description,
        "created_at": transaction.created_at
    } for transaction in transactions]), 200