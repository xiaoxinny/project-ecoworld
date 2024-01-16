class Item:
    def __init__(self, item_id, name, description, price, stock_count, dimensions, supplier):
        self.__item_id = item_id
        self.__description = description
        self.__price = price
        self.__stock_count = stock_count
        self.__dimensions = dimensions
        self.__supplier = supplier

    # accessors
    def get_item_id(self):
        return self.__.name

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_stock_count(self):
        return self.__
    
    def get_dimensions(self):
        return self.__dimensions

    # mutators
    def set_name(self, name):
        self.__name = name

    def set_description(self, description):
        self.__description = description

    def set_price(self, price):
        self.__price = price

    def set_stock_count(self, stock_count):
        self.__stock_count = stock_count

    def set_dimensions(self, dimensions):
        self.__dimensions = dimensions

    def set_supplier(self, supplier):
        self.__supplier = supplier 
