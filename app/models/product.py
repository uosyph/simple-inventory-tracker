from app import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    # Many-to-many relationship with Ingredient
    ingredients = db.relationship("ProductIngredient", backref="product", lazy=True)

    # Many-to-many relationship with Order via OrderItem
    order_items = db.relationship("OrderItem", backref="product", lazy=True)
