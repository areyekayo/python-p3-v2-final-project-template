from user import User
from expense import Expense
from __init__ import CONN, CURSOR

class Payment:
    all = {}

    def __init__(self, expense_id, recipient_id, ower_id, is_paid=0, payment_date=None, id=None):
        self.expense_id = expense_id
        self.recipient_id = recipient_id
        self.ower_id = ower_id
        self.payment_amount = self.calculate_payment_amount()
        self.is_paid = is_paid
        self.payment_date = payment_date
        self.id = id
    
    @property
    def expense_id(self):
        return self._expense_id
    
    @expense_id.setter
    def expense_id(self, expense_id):
        if type(expense_id) is int and Expense.find_by_id(expense_id):
            self._expense_id = expense_id
        else: raise ValueError("Expense ID must reference an expense in the database")

    @property
    def recipient_id(self):
        return self._recipient_id
    @recipient_id.setter
    def recipient_id(self, recipient_id):
        if type(recipient_id) is int and User.find_by_id(recipient_id):
            self._recipient_id = recipient_id
        else: raise ValueError("Recipient ID must reference a user in the database")
    
    @property
    def ower_id(self):
        return self._ower_id
    @ower_id.setter
    def ower_id(self, ower_id):
        if type(ower_id) is int and User.find_by_id(ower_id):
            self._ower_id = ower_id
        else: raise ValueError("Ower ID must reference a user in the database")
    


        
    


    

    

    



   
        
