import time
from collections import OrderedDict

from util.printable import Printable

class Vote(Printable):
    def __init__(self,anonymous,topic,description,options):
        self.anonymous = anonymous
        self.topic = topic
        self.description = description
        self.options = options

    def to_ordered_dict(self):
        return OrderedDict([('anonymous',self.anonymous),('topic',self.topic),('description',self.description),('options',self.options)])

    @classmethod
    def create_key(cls,user):
        k = str(user) + str(time.time())
        return abs(hash("logincode" + k))
        