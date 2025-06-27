from __init__ import CURSOR, CONN
import user

class Expense:

    all = []
    # Initialize a purchase category dict to store preferences to split bills proportionally or equally
    purchase_category_type = {"Groceries": "", "Restaurant": "", "Home Supplies": "", "Event": "", "Bar": ""}

    def __init__(self, purchase_date, purchase_category, store, expense_amount, payer, ower, is_settled=False):
        self.id = id
        self.purchase_date = purchase_date
        self.purchase_category = purchase_category
        self.store = store
        self.expense_amount = expense_amount
        self.payer = payer
        self.ower = ower
        self.is_settled = is_settled
        Expense.all.append(self)
    
    @property
    def purchase_category(self):
        return self._purchase_category
    
    @purchase_category.setter
    def purchase_category(self, purchase_category):
        if purchase_category not in Expense.purchase_category_type.keys():
            raise Exception("Purchase category not recognized")
        else:
            self._purchase_category = purchase_category
    
    @property
    def expense_amount(self):
        return self._expense_amount
    
    @expense_amount.setter
    def expense_amount(self, expense_amount):
        try: 
            expense_amount = float(expense_amount)
            self._expense_amount = expense_amount
        except: raise ValueError("Expense amount must be a dollar and cent amount: 12.34")
    
    @property
    def payer(self):
        return self._payer
    
    @payer.setter
    def payer(self, payer):
        if not isinstance(payer, User):
            raise ValueError("Payer is not a user")
        else:
            self._payer = payer
    
    @property
    def ower(self):
        return self._ower
    
    @ower.setter
    def ower(self, ower):
        if not isinstance(ower, User):
            raise ValueError("Ower is not a user")
        else:
            self._ower = ower

    
    

        

    
    

    
    


    
