import user
import expense
from __init__ import CONN, CURSOR

class Bill:
    all = []

    def __init__(self):
        self.expenses = self.get_unsettled_expenses()
        self.total = self.calculate_total()
        self.payer = self.calculate_payer()
        self.ower = self.calculate_ower()

    
    
