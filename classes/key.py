from collections import OrderedDict

from util.printable import Printable

class Key(Printable):
    def __init__(self,index,user,key):
        self.index = index
        self.user = user
        self.key = key

    def to_ordered_dict(self):
        return OrderedDict([('index',self.index),('user',self.user),('key',self.key)])