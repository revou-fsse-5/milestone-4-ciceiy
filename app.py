from flask import Flask
from extensions import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from controllers.user_controller import user_controller
from controllers.account_controller import account_controller
from controllers.transaction_controller import transaction_controller


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://milestone4_mastergrow:136cc95c9dd67609a863da5e6755be04e7fce9d7@92r5o.h.filess.io:3307/milestone4_mastergrow'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(user_controller)
app.register_blueprint(account_controller)
app.register_blueprint(transaction_controller)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)