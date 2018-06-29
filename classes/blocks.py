from time import time

from util.printable import Printable

class Block(Printable):
    def __init__(self,index,phash,content,proof,time=time()):
        self.index = index
        self.phash = phash
        self.timestamp = time
        self.content = content
        self.proof = proof