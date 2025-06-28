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

    def save(self):
        sql = """
            INSERT INTO expenses (purchase_date, store, expense_amount, payer_id, ower_id)
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.purchase_date, self.store, self.expense_amount, self.payer_id, self.ower_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        sql = """
            UPDATE expenses
            SET purchase_date = ?, store = ?, expense_amount = ?, payer_id = ?, ower_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.purchase_date, self.store, 
                             self.expense_amount, self.payer_id, self.ower_id, self.id))
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
    def create(cls, purchase_date, store, expense_amount, payer_id, ower_id):
        expense = cls(purchase_date, store, expense_amount, payer_id, ower_id)
        expense.save()
        return expense
    
    @classmethod
    def instance_from_db(cls, row):
        expense = cls.all.get(row[0])
        if expense:
            expense.purchase_date = row[1]
            expense.store = row[2]
            expense.expense_amount = row[3]
            expense.payer_id = row[4]
            expense.ower_id = row[5]
        else:
            expense = cls(row[1], row[2], row[3], row[4], row[5])
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
    
    
    


    
    

        

    
    

    
    


    
