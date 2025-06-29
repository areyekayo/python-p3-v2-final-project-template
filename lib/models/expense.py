from __init__ import CURSOR, CONN
from user import User
from datetime import datetime

class Expense:

    all = {}
    # Initialize a purchase category dict to store preferences to split bills proportionally or equally
    purchase_category_type = ["Groceries", "Restaurant", "Home Supplies", "Event", "Bar"]

    def __init__(self, purchase_date, purchase_category, store, expense_amount, payer_id, is_settled=0, settled_date=None, id=None):
        self.id = id
        self.purchase_date = purchase_date
        self.purchase_category = purchase_category
        self.store = store
        self.expense_amount = expense_amount
        self.payer_id = payer_id
        self.is_settled = is_settled
        self.settled_date = settled_date

    def __repr__(self):
        return (
            f"Expense: {self.purchase_date}, {self.purchase_category}, {self.store}, {self.expense_amount}, payer: {self.payer_id}, Is settled: {bool(self.is_settled)}"
        )

    @property
    def purchase_category(self):
        return self._purchase_category
    
    @purchase_category.setter
    def purchase_category(self, purchase_category):
        if purchase_category not in Expense.purchase_category_type:
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
    def payer_id(self, payer_id):
        if type(payer_id) is int and User.find_by_id(payer_id):
            self._payer_id = payer_id
        else:
            raise ValueError("Payer must reference a user in the database")
    
    # @property
    # def ower_id(self):
    #     return self._ower_id
    
    # @ower_id.setter
    # def ower_id(self, ower_id):
    #     if type(ower_id) is int and User.find_by_id(ower_id):
    #         self._ower_id = ower_id
    #     else:
    #         raise ValueError("Ower must reference a user in the database")
        
    @property
    def purchase_date(self):
        return self._purchase_date
    
    @purchase_date.setter
    def purchase_date(self, purchase_date):
        try:
            datetime.strptime(purchase_date, "%Y-%m-%d")
            self._purchase_date = purchase_date
        except: ValueError("Purchase Date must be in YYYY-MM-DD format")

    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS expenses (
            id  INTEGER PRIMARY KEY,
            purchase_date TEXT,
            purchase_category TEXT,
            store TEXT,
            expense_amount REAL,
            payer_id INTEGER,
            is_settled INTEGER,
            settled_date TEXT,
            FOREIGN KEY (payer_id) REFERENCES users(id)
        )
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

    def save(self):
        sql = """
            INSERT INTO expenses (purchase_date, purchase_category, store, expense_amount, payer_id, is_settled)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.purchase_date, self.purchase_category, self.store, self.expense_amount, self.payer_id, self.is_settled))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        sql = """
            UPDATE expenses
            SET purchase_date = ?, purchase_category = ?, store = ?, expense_amount = ?, payer_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.purchase_date, self.purchase_category, 
                             self.store, self.expense_amount, self.payer_id, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE from expenses
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, purchase_date, purchase_category, store, expense_amount, payer_id, is_settled):
        expense = cls(purchase_date, purchase_category, store, expense_amount, payer_id, is_settled)
        expense.save()
        return expense
    
    @classmethod
    def instance_from_db(cls, row):
        expense = cls.all.get(row[0])
        if expense:
            expense.purchase_date = row[1]
            expense.purchase_category = row[2]
            expense.store = row[3]
            expense.expense_amount = row[4]
            expense.payer_id = row[5]
            expense.is_settled = row[6]
        else:
            expense = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            expense.id = row[0]
            cls.all[expense.id] = expense
        return expense
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM expenses
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM expenses
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    # @classmethod
    # def find_all_by_ower_id(cls, ower_id):
    #     sql = """
    #         SELECT *
    #         FROM expenses
    #         WHERE ower_id = ?
    #     """
    #     rows = CURSOR.execute(sql, (ower_id,)).fetchall()

    #     return [cls.instance_from_db(row) for row in rows]
    
    @classmethod
    def find_unsettled_expenses(cls):
        sql = """
            SELECT *
            FROM expenses
            WHERE is_settled = 0
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def settle(self):
        sql = """
            UPDATE expenses
            SET is_settled = 1
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        self.is_settled = 1

    # @classmethod
    # def top_payer_amount(cls):
    #     payer_amount = {}
    #     for expense in cls.find_unsettled_expenses():
    #         payer_amount[expense.payer_id] = payer_amount.get(expense.payer_id, 0) + expense.expense_amount
        
        

    

    


    
    

        

    
    

    
    


    
