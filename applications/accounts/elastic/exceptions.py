
class StoreDoesNotExist(Exception):
    def __init__(self):

        super(ValidationError, self).__init__("Store with the given query does not exist")
