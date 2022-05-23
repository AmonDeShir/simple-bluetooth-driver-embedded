from pocha import after_each, describe, it
from unittest.mock import patch

from src.auth.auth import Auth
from src.secret.conf import Config


@describe('Auth')
def _():
    @after_each
    def _():
        Auth.CURRENT_SESSION = None


    @describe('check_password')
    def _():
        @it('should return true if password is correct')
        def _():
            assert Auth.check_password(Config.password)
        

        @it('should return false if password is incorrect')
        def _():
            assert not Auth.check_password('incorrect password')


    @describe('clear_session')
    def _():
        @it('should clear the current session')
        def _():
            Auth.CURRENT_SESSION = 'current-ID'
            Auth.clear_session()
            assert Auth.CURRENT_SESSION == None


    @describe('create_session')
    def _():
        @it('should return a new session ID')
        @patch('src.auth.auth.nanoid.generate')
        def _(generate):
            generate.return_value = 'new-ID'
            assert Auth.create_session() == 'new-ID'

        
        @it('should replace an existing session ID with a new one')
        @patch('src.auth.auth.nanoid.generate')
        def _(generate):
            Auth.CURRENT_SESSION = 'old-ID'
            generate.return_value = 'new-ID'
            
            Auth.create_session()
            assert Auth.CURRENT_SESSION == 'new-ID'