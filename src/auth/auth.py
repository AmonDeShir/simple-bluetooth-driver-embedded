from src.secret.conf import Config
import nanoid

class Auth:
    CURRENT_SESSION = None

    @staticmethod
    def check_password(password):
        if password == Config.password:
            return True
        else:
            return False


    @staticmethod
    def verify_session(session):
        if Auth.CURRENT_SESSION == None:
            return False

        return session == Auth.CURRENT_SESSION


    @staticmethod
    def clear_session():
        Auth.CURRENT_SESSION = None


    @staticmethod
    def create_session():
        Auth.CURRENT_SESSION = nanoid.generate()
        return Auth.CURRENT_SESSION