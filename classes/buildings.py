from collections import OrderedDict

from util.printable import Printable

class Buildings(Printable):
    def __init__(self,ID,current,t_1,t_2,t_3,t_4,t_5,t_6,t_7,m2,location,rent,amortization,maintenance,year,own=False):
        self.id = ID
        self.current = current
        self.t_1 = t_1
        self.t_2 = t_2
        self.t_3 = t_2
        self.t_4 = t_4
        self.t_5 = t_5
        self.t_6 = t_6
        self.t_7 = t_7
        self.m2 = m2
        self.location = location
        self.rent = rent
        self.amortization = amortization
        self.maintenance = maintenance
        self.year = year
        self.own = own

    def to_ordered_dict(self):
        return OrderedDict([('ID',self.id),('current',self.current),('t_1',self.t_1),('t_2',self.t_2),('t_3',self.t_3),('t_4',self.t_4),('t_5',self.t_5),('t_6',self.t_6),('t_7',self.t_7),('m2',self.m2),('location',self.location),('rent',self.rent),('amortization',self.amortization),('maintenance',self.maintenance),('year',self.year),('own',self.own)])
