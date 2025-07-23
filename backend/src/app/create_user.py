from models import db, User
from flask import Flask
from config import Config
from passlib.hash import bcrypt
from sqlalchemy import inspect

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_user(username, password):
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('users'):
            db.create_all()

        if User.query.filter_by(username=username).first():
            print(f"User '{username}' already exists.")
        else:
            hashed = bcrypt.hash(password)
            user = User(username=username, password_hash=hashed)
            db.session.add(user)
            db.session.commit()
            print(f"User '{username}' created.")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Create a new user.')
    parser.add_argument('username', type=str, help='Username')
    parser.add_argument('password', type=str, help='Password')
    args = parser.parse_args()

    create_user(args.username, args.password)
