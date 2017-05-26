import uuid
from src.common.utils import Utils
from src.common.database import Database
import src.models.users.errors as UserErrors
import src.models.users.constants as UsersConstansts
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        validate email and password if they are related to each other
        :param email: user_email's email
        :param password: A sha512 hashed password
        :return: true if valid, False otherwise
        """
        user_data = Database.find_one(UsersConstansts.COLLECTION,{"email": email})

        if user_data is None:
            # invalid login credentials
            raise UserErrors.UserNotExistsError("User Does Not Exists.")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Invalid password")

        return True

    @staticmethod
    def register_user(email, password):
        user_data = Database.find_one(UsersConstansts.COLLECTION, {"email": email})

        if user_data is not None:
            # raise error
            raise UserErrors.UserAlreadyRegisteredError("Already Registered e-mail!")
        if not Utils.email_is_valid(email):
            # raise error
            raise UserErrors.InvalidEmailError("Invalid e-mail!")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
                "_id": self._id,
                "email": self.email,
                "password": self.password
                }

    @classmethod
    def find_by_email(cls,email):
        return cls(**Database.find_one(UsersConstansts.COLLECTION,{'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)