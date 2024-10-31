from flask import Blueprint, request, jsonify
from models.account_model import Account
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

account_controller = Blueprint('account_controller', __name__)

@account_controller.route('/account', methods=['POST'])
@jwt_required()
def create_account():
    current_user_id = get_jwt_identity()
    data = request.json
    new_account = Account(
        user_id=current_user_id,
        account_type=data['account_type'],
        account_number=data['account_number'],
        balance=data.get('balance', 0.0)
    )
    db.session.add(new_account)
    db.session.commit()
    return {"message": "Account created"}, 201

@account_controller.route('/account', methods=['GET'])
@jwt_required()
def get_accounts():
    current_user_id = get_jwt_identity()
    accounts = Account.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        "id": account.id,
        "account_type": account.account_type,
        "account_number": account.account_number,
        "balance": float(account.balance)
    } for account in accounts]), 200

@account_controller.route('/account/<int:id>', methods=['PUT'])
@jwt_required()
def update_account(id):
    data = request.json
    account = Account.query.get(id)
    
    if not account:
        return {"message": "Account not found"}, 404
    
    account.account_type = data.get('account_type', account.account_type)
    account.balance = data.get('balance', account.balance)
    db.session.commit()
    return {"message": "Account updated"}, 200

@account_controller.route('/account/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_account(id):
    account = Account.query.get(id)
    
    if not account:
        return {"message": "Account not found"}, 404
    
    db.session.delete(account)
    db.session.commit()
    return {"message": "Account deleted"}, 200