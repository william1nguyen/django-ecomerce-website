import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv('.env')

SECRET_KEY =  os.environ.get('SECRET_KEY')

def create_jwt_token(user_id):
    expiration_time = datetime.utcnow() + timedelta(days=1)  # Token expiration time
    token = jwt.encode({'user_id': user_id, 'exp': expiration_time}, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is invalid
