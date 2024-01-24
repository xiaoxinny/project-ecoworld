class User:

    def __init__(self, name, email, salt, password, ip_address):
        self.__name = name
        self.__email = email
        self.__salt = salt  # salt is used to hash the password
        self.__hashed_password = password
        self.__ip_address = ip_address


    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_salt(self):
        return self.__salt

    def get_password(self):
        return self.__hashed_password

    def get_ip_address(self):
        return self.__ip_address

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password):
        self.__hashed_password = password

    def set_ip_address(self, ip_address):
        self.__ip_address = ip_address


class Staff(User):

    def __init__(self, name, email, salt, password, ip_address, staff_id):
        super().__init__(name, email, salt, password, ip_address)
        self.__staff_id = staff_id
