from pocha import after, before_each, describe, it
from unittest.mock import MagicMock, patch

from src.auth.auth_router import AuthRouter, authenticate

@describe('AuthRouter')
def _():
    @describe('init')
    def _():
        @it('should set up bluetooth event listeners')
        def _():
            bluetooth = MagicMock()
            AuthRouter(bluetooth)
            
            assert bluetooth.on.call_count == 1
            assert bluetooth.on.call_args[0][0] == 'log-in'
    

    @describe('log_in')
    def _():
        @it('should emit log-in-success if password is correct')
        @patch('src.auth.auth_router.Auth')
        def _(Auth):
            bluetooth = MagicMock()
            Auth.check_password.return_value = True
            Auth.generate_token.return_value = "token"

            auth_router = AuthRouter(bluetooth)
            auth_router.log_in('correct password')
            bluetooth.emit.assert_called_with("log-in-success:token")
    

        @it('should emit log-in-failure if password is incorrect')
        @patch('src.auth.auth_router.Auth')
        def _(Auth):
            bluetooth = MagicMock()
            Auth.check_password.return_value = False

            auth_router = AuthRouter(bluetooth)
            auth_router.log_in('incorrect password')
            bluetooth.emit.assert_called_with("log-in-failure")


@describe('authenticate')
def _():
    class Test:
        def __init__(self):
            self.called = False
            self.bluetooth = MagicMock()
            self.args = None

        @authenticate('operation')
        def test_function(self, args):
            self.called = True
            self.args = args


    @it('should emit operation-failure:unauthorized if the token if there are no arguments')
    @patch('src.auth.auth_router.Auth')
    def _(Auth):
        Auth.check_token.return_value = True

        test = Test()
        test.test_function(None)
        assert test.called == False
        test.bluetooth.emit.assert_called_with("operation-failure:unauthorized")


    @it('should call the decorated function if the token is valid')
    @patch('src.auth.auth_router.Auth')
    def _(Auth):
        Auth.check_token.return_value = True

        test = Test()
        test.test_function("token")
        assert test.called == True
        assert test.bluetooth.emit.call_count == 0
    
    
    @it('should emit operation-failure:unauthorized if the token is invalid')
    @patch('src.auth.auth_router.Auth')
    def _(Auth):
        Auth.check_token.return_value = False

        test = Test()
        test.test_function("token")
        assert test.called == False
        test.bluetooth.emit.assert_called_with("operation-failure:unauthorized")


    @it('should call the decorated function with arguments')
    @patch('src.auth.auth_router.Auth')
    def _(Auth):
        Auth.check_token.return_value = True

        test = Test()
        test.test_function("token, second argument, third argument")
        assert test.called == True
        assert test.args == "second argument, third argument"


    @it('should call the decorated function with None if there are no arguments')
    @patch('src.auth.auth_router.Auth')
    def _(Auth):
        Auth.check_token.return_value = True

        test = Test()
        test.test_function("token")
        assert test.called == True
        assert test.args == None
