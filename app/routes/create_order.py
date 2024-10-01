from app import app, db, Product, Order, OrderItem, Ingredient, ProductIngredient
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request data."}), 400

    try:
        # Step 1: Create the order
        order = Order()
        db.session.add(order)
        db.session.flush()

        # Step 2: Loop through products and add them to the order
        products_ordered = data.get("products", [])
        for item in products_ordered:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 1)

            if quantity < 1:
                return jsonify({"error": "Quantity cannot be less than 1."}), 400

            # Fetch the product
            product = db.session.get(Product, product_id)
            if not product:
                return (
                    jsonify({"error": f"Product with ID {product_id} not found."}),
                    404,
                )

            # Add product to order
            order_item = OrderItem(
                order_id=order.id, product_id=product.id, quantity=quantity
            )
            db.session.add(order_item)

            # Step 3: Check if there is enough stock for each product's ingredients
            for product_ingredient in product.ingredients:
                ingredient = db.session.get(Ingredient, product_ingredient.ingredient_id)
                used_amount = product_ingredient.amount * quantity

                # Check if there is sufficient stock
                if ingredient.stock < used_amount:
                    return jsonify(
                            {"error": f"Insufficient stock for ingredient {ingredient.name}."}), 400

                # If there is sufficient stock, deduct the amount
                ingredient.stock -= used_amount

                # Step 4: Check if stock falls below 50% and trigger email
                if ingredient.stock <= ingredient.initial_stock * 0.5:
                    if not ingredient.below_threshold:
                        # send_low_stock_email(ingredient)
                        print(ingredient)
                        ingredient.below_threshold = True

                db.session.add(ingredient)

        db.session.commit()
        return jsonify({"message": "Order placed successfully"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
