from models.__init__ import CONN, CURSOR

class User:

    all = {}
    total_income = 0

    def __init__(self, name, income, id=None):
        self.id = id
        self.name = name
        self.income = income

    # def __repr__(self):
    #     return (
    #         f"{self.name}, income: {self.income}"
    #     )
    
    @property
    def name(self):
        return self._name 
    @name.setter
    def name(self, name):
        if isinstance(name, str) and len(name):
            self._name = name
        else:
            raise ValueError("User name must be a non-empty string")
    
    @property
    def income(self):
        return self._income
    @income.setter
    def income(self, income):
        try: 
            income = int(income)
            self._income = income
        except: raise ValueError("Income must be an integer with no commas or decimals, ex: 50000")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            income INT)
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS users
        """
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
            INSERT INTO users (name, income)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.income))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, income):
        user = cls(name, income)
        user.save()
        return user
    

    @classmethod
    def instance_from_db(cls, row):
        user = cls.all.get(row[0])
        if user:
            user.name = row[1]
            user.income = row[2]
        else:
            user = cls(row[1], row[2])
            user.id = row[0]
            cls.all[user.id] = user
        return user
    
    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM users
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM users
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_from_db(row) if row else None
    
    def update(self):
        sql = """
            UPDATE users
            SET name = ?, income = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.income, self.id))
        CONN.commit()

    def delete(self):
        sql = """
            DELETE FROM users
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        del type(self).all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM users
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    def expenses(self):
        """Gets the expenses that the user paid for."""
        from models.expense import Expense
        sql = """
            SELECT * FROM expenses
            WHERE payer_id = ?
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Expense.instance_from_db(row) for row in rows]
    
    def get_unsettled_expenses(self):
        return [expense for expense in self.expenses() if expense.is_settled == 0]
    
    @classmethod
    def get_users_by_id(cls, user_list):
        return {id: User.find_by_id(id) for id in user_list}
    
    def get_owed_payments(self):
        from models.payment import Payment
        sql = """
            SELECT * FROM payments
            WHERE ower_id = ? AND is_paid = 0
        """
        CURSOR.execute(sql, (self.id,))
        rows = CURSOR.fetchall()
        return [Payment.instance_from_db(row) for row in rows]

        
    

        
    
        
        
    