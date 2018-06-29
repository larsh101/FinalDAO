from collections import OrderedDict

from util.printable import Printable

class Voted(Printable):
    def __init__(self,index,user,vote):
        self.index = index
        self.user = user
        self.vote = vote

    def to_ordered_dict(self):
        return OrderedDict([('index',self.index),('user',self.user),('vote',self.vote)])