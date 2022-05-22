from fake import fake
fake.use_fakes()

from src.secret.conf import Config
import time
import jwt


class Auth:
    def check_password(password):
        if password == Config.password:
            return True
        else:
            return False


    def check_token(token):
        try:
            jwt.decode(token, Config.jwt_secret, algorithms=['HS256'])
            
            return True
        except Exception:
            return False


    def generate_token():
        expired_time = Config.jwt_exp + time.time()
        return jwt.encode({"exp": expired_time}, Config.jwt_secret)
