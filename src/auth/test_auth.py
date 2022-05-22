from pocha import after, before_each, after_each, describe, it
from unittest.mock import MagicMock

from src.auth.auth import Auth
from src.secret.conf import Config
import jwt


def raise_(ex):
    raise ex

@describe('Auth')
def _():
    @describe('check_password')
    def _():
        @it('should return true if password is correct')
        def _():
            assert Auth.check_password(Config.password)
        

        @it('should return false if password is incorrect')
        def _():
            assert not Auth.check_password('incorrect password')


    @describe('check_token')
    def _():
        origin = jwt.decode

        @after
        def _():
            jwt.decode = origin


        @it('should return true if token is correct')
        def _():
            jwt.decode = lambda _, __, algorithms : True
            assert Auth.check_token('correct token')


        @it('should return false if token is incorrect')
        def _():
            jwt.decode = lambda _, __, algorithms : raise_(Exception("Invalid token"))
            assert not Auth.check_token('incorrect token')

    
    @describe('generate_token')
    def _():
        @it('should return a new correct decodable token')
        def _():
            token = Auth.generate_token()
            assert jwt.decode(token, Config.jwt_secret, algorithms=['HS256'])