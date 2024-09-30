from app import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Float, nullable=False)  # Stock in kilograms
    initial_stock = db.Column(db.Float, nullable=False)  # Initial Stock in kilograms
    below_threshold = db.Column(db.Boolean, default=False)

    # Many-to-many relationship with Product
    products = db.relationship("ProductIngredient", backref="ingredient", lazy=True)
