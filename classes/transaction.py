from collections import OrderedDict

from util.printable import Printable

class Transaction(Printable):
    def __init__(self,sender,recipient,amount,kind):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.kind = kind

    def to_ordered_dict(self):
        return OrderedDict([('sender',self.sender),('recipient',self.recipient),('amount',self.amount),('kind',self.kind)])