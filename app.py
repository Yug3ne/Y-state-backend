# from flask import Flask
# from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt

# import os
# import secrets

# from utils.dbconfig import db
# from routes.auth import auth_bp

# app = Flask(__name__)

# flask_secret_key = secrets.token_urlsafe(16)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = flask_secret_key

# db.init_app(app)
# migrate = Migrate(app,db)
# bcrypt = Bcrypt(app)


# app.register_blueprint(auth_bp)

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)

# server/app.py
from server import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8080)
