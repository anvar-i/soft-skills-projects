class User:
    def __init__(self, user_id: str, username: str, password_hash : str, password_salt: str):
        self.user = user_id 
        self.username = username
        self.__password_hash__ = password_hash
        self.password_salt = password_salt
class Terminal:
    pass
                                                                                                        