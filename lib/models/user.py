from __init__ import CONN, CURSOR

class User:

    all = []

    def __init__(self, name, income):
        self.id = id
        self.name = name
        self.income = income
    
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
    
        
        
    