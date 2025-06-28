from __init__ import CURSOR, CONN
from user import User

class Expense:

    all = []
    # Initialize a purchase category dict to store preferences to split bills proportionally or equally
    purchase_category_type = {"Groceries": "", "Restaurant": "", "Home Supplies": "", "Event": "", "Bar": ""}

    def __init__(self, purchase_date, purchase_category, store, expense_amount, payer_id, ower_id, is_settled=False):
        self.id = id
        self.purchase_date = purchase_date
        self.purchase_category = purchase_category
        self.store = store
        self.expense_amount = expense_amount
        self.payer_id = payer_id
        self.ower_id = ower_id
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
    def payer_id(self):
        return self._payer_id
    
    @payer_id.setter
    def payer(self, payer_id):
        if type(payer_id) is int and User.find_by_id(payer_id):
            self._payer_id = payer_id
        else:
            raise ValueError("Payer must reference a user in the database")
    
    @property
    def ower_id(self):
        return self._ower_id
    
    @ower_id.setter
    def ower_id(self, ower_id):
        if type(ower_id) is int and User.find_by_id(ower_id):
            self._ower_id = ower_id
        else:
            raise ValueError("Payer must reference a user in the database")
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS expenses (
            id  INTEGER PRIMARY KEY,
            purchase_date TEXT,
            store TEXT,
            expense_amount REAL,
            payer_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES users(id)),
            ower_id INTEGER,
            FOREIGN KEY (ower_id) REFERENCES users(id))
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS expenses;
        """
        CURSOR.execute(sql)
        CONN.commit()

    


    
    

        

    
    

    
    


    
