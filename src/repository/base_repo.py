from helpers import get_logger,get_settings
class Base:
    def __init__(self,db):
        self.db=db
        self.logger=get_logger(self.__class__.__name__)
        self.settings=get_settings()