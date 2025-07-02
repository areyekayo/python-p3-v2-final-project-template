from models.user import User
from datetime import date
from models.__init__ import CONN, CURSOR

class Payment:
    all = {}

    def __init__(self, expense_id, recipient_id, ower_id, payment_amount, is_paid=0, paid_date=None, id=None):
        self.expense_id = expense_id
        self.recipient_id = recipient_id
        self.ower_id = ower_id
        self.payment_amount = payment_amount
        self.is_paid = is_paid
        self.paid_date = paid_date
        self.id = id
    
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

    @property
    def payment_amount(self):
        return self._payment_amount
    @payment_amount.setter
    def payment_amount(self, payment_amount):
        try:
            payment_amount = float(payment_amount)
            self._payment_amount = payment_amount
        except: raise ValueError("Payment amount must be a dollar and cent amount: 12.34")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY,
            expense_id INTEGER,
            recipient_id INTEGER,
            ower_id INTEGER,
            payment_amount REAL,
            is_paid INTEGER,
            paid_date TEXT,
            FOREIGN KEY (expense_id) REFERENCES expenses(id),
            FOREIGN KEY (recipient_id) REFERENCES users(id),
            FOREIGN KEY (ower_id) REFERENCES users(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS payments
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO payments (expense_id, recipient_id, ower_id, payment_amount, is_paid, paid_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.expense_id, self.recipient_id, self.ower_id,
                            self.payment_amount, self.is_paid, self.paid_date))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def delete(self):
        sql = """
            DELETE FROM payments
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None


    @classmethod
    def create(cls, expense_id, recipient_id, ower_id, payment_amount, is_paid=0, paid_date=None):
        payment = cls(expense_id, recipient_id, ower_id, payment_amount, is_paid, paid_date)
        payment.save()
        return payment
    
    @classmethod
    def instance_from_db(cls, row):
        payment = cls.all.get(row[0])
        if payment:
            payment.expense_id = row[1]
            payment.recipient_id = row[2]
            payment.ower_id = row[3]
            payment.payment_amount = row[4]
            payment.is_paid = row[5]
            payment.paid_date = row[6]
        else:
            payment = cls(row[1], row[2], row[3], row[4], row[5], row[6])
            payment.id = row[0]
            cls.all[payment.id] = payment
        return payment
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM payments
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]
    
    def settle_payment(self):
        sql = """
            UPDATE payments
            SET is_paid = ?, paid_date = ?
            WHERE id = ?
        """
        self.is_paid = 1
        self.paid_date = date.today().strftime("%Y-%m-%d")
        CURSOR.execute(sql, (self.is_paid, self.paid_date, self.id))
        CONN.commit()

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM payments
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None