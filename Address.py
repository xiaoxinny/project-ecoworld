class Address:
    class User:
        count_id = 0

        def __init__(self, name, address, postal_code, email_address, contact_number):
            address.count_id += 1
            self.__name = name
            self.__email_address = email_address
            self.__contact_number = contact_number
            self.__address = address
            self.__postal_code = postal_code

        def get_address_id(self):
            return self.__address_id

        def get_name(self):
            return self.__name

        def get_email_address(self):
            return self.__email_address

        def get_contact_number(self):
            return self.__contact_number

        def get_address(self):
            return self.__address

        def get_postal_code(self):
            return self.__postal_code

        def set_user_id(self, user_id):
            self.__user_id = user_id

        def set_name(self, name):
            self.__name = name

        def set_email_address(self, email_address):
            self.__email_address = email_address

        def set_contact_number(self, contact_number):
            self.__contact_number = contact_number

        def set_address(self, address):
            self.__address = address

        def set_postal_code(self, postal_code):
            self.__postal_code = postal_code

        def __str__(self):
            return self.__contact_number