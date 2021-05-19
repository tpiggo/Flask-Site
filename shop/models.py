from flask_sqlalchemy import SQLAlchemy

# instantiating the application connection to the database through lazy
# instantiation
shop_db = SQLAlchemy()


class Person(shop_db.Model):
    id = shop_db.Column(shop_db.Integer, nullable=True, primary_key=True)
    first_name = shop_db.Column(shop_db.String(50), nullable=True)
    last_name = shop_db.Column(shop_db.String(50), nullable=True)
    email = shop_db.Column(shop_db.String(50), nullable=True)
    gender = shop_db.Column(shop_db.String(50), nullable=True)
    country_of_birth = shop_db.Column(shop_db.String(50), nullable=True)
    date_of_birth = shop_db.Column(shop_db.DateTime, nullable=True)

    def __repr__(self):
        return "<Person %r %r>" % (self.first_name, self.last_name)


class Grocerystore(shop_db.Model):
    id = shop_db.Column(shop_db.Integer, nullable=False, primary_key=True)
    person_id = shop_db.Column(shop_db.Integer, nullable=False)
    amount = shop_db.Column(shop_db.Float, nullable=False)
    type_of_payment = shop_db.Column(shop_db.String(25), nullable=False)

    def __repr__(self):
        return "<Grocery Store Record: %r %r %r>" % (
            self.id,
            self.type_of_payment,
            self.amount
        )

    def get_as_dict(self):
        return {
            "type" : "grocerystore", 
            "id": self.id, 
            "person_id": self.person_id,
            "type_of_payment": self.type_of_payment, 
            "amount": self.amount
            }

class Hardwarestore(shop_db.Model):
    id = shop_db.Column(shop_db.Integer, nullable=False, primary_key=True)
    person_id = shop_db.Column(shop_db.Integer, nullable=False)
    amount = shop_db.Column(shop_db.Float, nullable=False)
    type_of_payment = shop_db.Column(shop_db.String(25), nullable=False)

    def __repr__(self):
        return "<Hardware Store Record: %r %r %r>" % (
            self.id,
            self.type_of_payment,
            self.amount
        )

    def get_as_dict(self):
        return {
            "type" : "hardwarestore", 
            "id": self.id, 
            "person_id": self.person_id,
            "type_of_payment": self.type_of_payment, 
            "amount": self.amount
            }

class Appearlstore(shop_db.Model):
    id = shop_db.Column(shop_db.Integer, nullable=False, primary_key=True)
    person_id = shop_db.Column(shop_db.Integer, nullable=False)
    amount = shop_db.Column(shop_db.Float, nullable=False)
    type_of_payment = shop_db.Column(shop_db.String(25), nullable=False)

    def __repr__(self):
        return "<Appearl Store Record: %r %r %r>" % (
            self.id,
            self.type_of_payment,
            self.amount
        )

    def get_as_dict(self):  
        return {
            "type" : "appearlstore", 
            "id": self.id,
            "person_id": self.person_id,
            "type_of_payment": self.type_of_payment, 
            "amount": self.amount
            }