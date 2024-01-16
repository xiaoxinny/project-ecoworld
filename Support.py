class Support:
    def __init__(self, name, email, summary):
        self.__name = name
        self.__email = email
        self.__summary = summary

    #  accessors
    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_summary(self):
        return self.__summary

    # mutators
    def set_name(self, name):
        self.__name = name  

    def set_email(self, email):
        self.__email = email

    def set_summary(self, summary):
        self.__summary = summary
        