class Address:
    def __init__(self, name, phone_number, address, postal_code):
        self.__name = name
        self.__phone_number = phone_number
        self.__address = address
        self.__postal_code = postal_code
        
    # accessors
    def get_name(self):
        return self.__name
    
    def get_phone_number(self):
        return self.__phone_number
    
    def get_address(self):
        return self.__address
    
    def get_postal_code(self):
        return self.__postal_code
    
    # mutators
    def set_name(self, name):
        self.__name = name
    
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
        
    def set_address(self, address):
        self.__address = address
        
    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code
        