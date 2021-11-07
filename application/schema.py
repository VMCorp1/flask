from application import *

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    pubyear = db.Column(db.Integer)
    price = db.Column(db.Integer)

    def __init__(self, title, author, pubyear, price):
        self.title = title
        self.author = author
        self.pubyear = pubyear
        self.price = price


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    pubyear = db.Column(db.Integer)
    price = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    orderid = db.Column(db.String(50), db.ForeignKey('orders.id'))

    def __init__(self, title, author, pubyear, price, quantity, orderid):
        self.title = title
        self.author = author
        self.pubyear = pubyear
        self.price = price
        self.quantity = quantity
        self.orderid = orderid


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(25))
    address = db.Column(db.String(100))
    orderid = db.Column(db.String(50), unique=True)
    created = db.Column(db.Integer)

    def __init__(self, name, email, phone, address, orderid, created):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.orderid = orderid
        self.created = created


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, login, password):
        self.login = login
        self.password = password
