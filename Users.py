class User:

    def __init__(self, name, email, password, identity, ip_address):
        self.__name = name
        self.__email = email
        self.__password = password
        self.__identity = identity
        self.__ip_address = ip_address

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_password(self):
        return self.__password

    def get_identity(self):
        return self.__identity

    def get_ip_address(self):
        return self.__ip_address

    def set_name(self, name):
        self.__name = name

