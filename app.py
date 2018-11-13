from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
import datetime
from datetime import timedelta
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from resources.profile import Profile, ProfileList
from models.user import UserModel

from resources.user import UserRegister, UserList
from security import authenticate, identity
from re_usable import gen_send_otp, otp_check


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisisthesecretkey'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()



jwt = JWT(app, authenticate, identity)


api.add_resource(UserRegister, '/signup')
api.add_resource(Profile, '/profile/<string:name>')
api.add_resource(UserList, '/users')
api.add_resource(ProfileList, '/profiles')


@app.route('/reset', methods=["POST"])
def reset():
    data = UserRegister.parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    res = otp_check(data["otp"], user)
    if res[0] and res[1]:
        user.password = data["password"]
        user.save_to_db()
        return jsonify({"message": "OTP matched"})
    elif res[1] == False:
        return jsonify({"message": "OTP has expired. ask for /resend"})
    return jsonify({"message": "OTP not matched. try /forgot again"})




@app.route('/forgot', methods=["POST"])
def forgot_password():
    data = UserRegister.parser.parse_args()
    user = UserModel.find_by_username(data['username'])
    if user is None:
        return ("user of this name doesn't exist")
    user.otp = gen_send_otp(user, confirm)
    user.otp_sent = datetime.datetime.now()
    user.save_to_db()
    return jsonify({"message":"OTP has been sent to your mail"})


@app.route('/resend', methods= ["POST"])
def call_forgot():
    forgot_password()
    return jsonify({"message":"OTP has been sent to your mail"})


@app.route('/confirm', methods=['POST'])
def confirm():
    data = UserRegister.parser.parse_args()
    user = UserModel.find_by_username(data["username"])
    res = otp_check(data["otp"], user)
    print(res)
    if res[0] and res[1]:
        return jsonify({"message": "OTP matched"})
    elif res[1] == False and res[0] == True:
        return jsonify({"message" : "OTP has expired. ask for /resend"})
    return jsonify({"message": "OTP not matched"})

@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'refresh_token': create_refresh_token(identity=current_user)
          }
    return jsonify(ret), 200


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)