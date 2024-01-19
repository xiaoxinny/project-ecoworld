class User:

    def __init__(self, name, email, salt, password, identity, ip_address):
        self.__name = name
        self.__email = email
        self.__salt = salt  # salt is used to hash the password
        self.__password = password
        self.__identity = identity
        self.__ip_address = ip_address
        self.__salt_hash = self.__salt + self.__password

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_salt(self):
        return self.__salt

    def get_salt_hash(self):
        return self.__salt + self.__password

    def get_password(self):
        return self.__password

    def get_identity(self):
        return self.__identity

    def get_ip_address(self):
        return self.__ip_address

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_salt(self, salt):
        self.__salt = salt  # salt is used to hash the password
        self.__salt_hash = self.__salt + self.__password

    def set_password(self, password):
        self.__password = password

    def set_identity(self, identity):
        self.__identity = identity

    def set_ip_address(self, ip_address):
        self.__ip_address = ip_address


class Staff(User):

    def __init__(self, name, email, salt, password, identity, ip_address):
        super().__init__(name, email, salt, password, identity, ip_address)
        self.__is_admin = True
