from flask import Blueprint, request, jsonify,make_response
from flask_restful import Resource,Api
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, current_user,get_jwt_identity
from server.utils.dbconfig import db
from server import bcrypt
from server.models.user import User
from server.models.tokenBlocklist import TokenBlocklist

auth_bp = Blueprint('auth', __name__)
auth_api = Api(auth_bp)


# def check_if_token_in_blocklist(jwt_header, jwt_payload):
#     jti = jwt_payload['jti']
#     token = TokenBlocklist.query.filter_by(jti=jti).first()
#     return token is not None

class userRegistration(Resource):
    def post(self):
      
        try:
            data = request.get_json()
              # Check if the user already exists in the database
            if User.query.filter_by(email=data['email']).first() is not None:
                return make_response({"Message": 'User with this email already exists'}, 401)
            if User.query.filter_by(username=data['username']).first() is not None:
                return make_response({"Message": 'User with this username already exists'}, 401)
            
            
        # Post the user registration details to the database
            new_user = User(
                id = data['id'],
                email = data['email'],
                username = data['username'],
                password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),       
            )
            db.session.add(new_user)
            db.session.commit()
            response_body = {'Message': f'User {new_user.username} has been created successfully'}
            return make_response((response_body), 201)
        except KeyError as e:
            return make_response({'Error': f'Missing key: {str(e)}'},400)
        except Exception as e:
            db.session.rollback()
            return make_response({'Error': str(e)}, 500)

    
class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                token = create_access_token(identity=user.id)
                response_body = {"token": token, "username":user.username, "user_id":user.id}
                return make_response(response_body, 200)
            else:
                return make_response({"Message": "Invalid credentials"}, 401)
            
        except Exception as e:
            return make_response({"Message": str(e)},500)

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        try:
            jti = get_jwt()['jti']
            # Add token to blocklist
            token_blocklist = TokenBlocklist(jti=jti)
            db.session.add(token_blocklist)
            db.session.commit()

            return make_response(jsonify({"Message": "Successfully logged out"}), 200)
        
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"Message": str(e)}), 500)

class Protected(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user).first()
            if not user:
                return jsonify({"message": "User not found"}), 404
            return make_response({"message": f"Logged in as {user.username}"},200)
        except Exception as e:
            return jsonify({"message": str(e)}), 500
        

auth_api.add_resource(userRegistration, '/signup')
auth_api.add_resource(UserLogin, '/login')
auth_api.add_resource(UserLogout, '/logout')
auth_api.add_resource(Protected, '/protected')