from app import db


class ProductIngredient(db.Model):
    __tablename__ = "product_ingredient"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredients.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # Amount of ingredient in grams
