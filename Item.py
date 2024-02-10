class Item:
    def __init__(self, photo, item_id, name, description, price, stock_count, dimensions, supplier, category):
        self.__photo = photo
        self.__item_id = item_id
        self.__name = name
        self.__description = description
        self.__price = price
        self.__stock_count = stock_count
        self.__dimensions = dimensions
        self.__supplier = supplier
        self.__category = category

    # accessors
    def get_photo(self):
        return self.__photo

    def get_item_id(self):
        return self.__item_id

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_price(self):
        return self.__price

    def get_stock_count(self):
        return self.__stock_count

    def get_dimensions(self):
        return self.__dimensions

    def get_supplier(self):
        return self.__supplier

    def get_category(self):
        return self.__category

    # mutators
    def set_photo(self, photo):
        self.__photo = photo

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

    def set_category(self):
        return self.__category
