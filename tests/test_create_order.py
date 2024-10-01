from app import db, Product, Ingredient, ProductIngredient


def test_create_order(client):
    ingredient1 = Ingredient(name="Beef", stock=20, initial_stock=20)
    ingredient2 = Ingredient(name="Cheese", stock=5, initial_stock=5)
    ingredient3 = Ingredient(name="Onion", stock=1, initial_stock=1)

    product1 = Product(name="Burger")

    db.session.add_all([ingredient1, ingredient2, ingredient3, product1])
    db.session.commit()

    db.session.add(
        ProductIngredient(
            product_id=product1.id, ingredient_id=ingredient1.id, amount=0.15
        )
    )  # 150g Beef
    db.session.add(
        ProductIngredient(
            product_id=product1.id, ingredient_id=ingredient2.id, amount=0.03
        )
    )  # 30g Cheese
    db.session.add(
        ProductIngredient(
            product_id=product1.id, ingredient_id=ingredient3.id, amount=0.02
        )
    )  # 20g Onion
    db.session.commit()

    # Order 2 Burgers
    response = client.post(
        "/orders",
        json={"products": [{"product_id": product1.id, "quantity": 2}]},
    )

    assert response.status_code == 201
    assert response.json["message"] == "Order placed successfully"

    # Verify that ingredient stock has been updated correctly
    beef = Ingredient.query.filter_by(name="Beef").first()
    cheese = Ingredient.query.filter_by(name="Cheese").first()
    onion = Ingredient.query.filter_by(name="Onion").first()

    assert beef.stock == 20 - (0.15 * 2)  # 150g * 2
    assert cheese.stock == 5 - (0.03 * 2)  # 30g * 2
    assert onion.stock == 1 - (0.02 * 2)  # 20g * 2


def test_order_product_not_found(client):
    response = client.post(
        "/orders",
        json={"products": [{"product_id": 999, "quantity": 2}]},
    )

    assert response.status_code == 404
    assert response.json["error"] == "Product with ID 999 not found."


def test_order_with_zero_quantity(client):
    ingredient1 = Ingredient(name="Beef", stock=20, initial_stock=20)
    product1 = Product(name="Burger")

    db.session.add_all([ingredient1, product1])
    db.session.commit()
    db.session.add(
        ProductIngredient(
            product_id=product1.id, ingredient_id=ingredient1.id, amount=0.15
        )
    )
    db.session.commit()

    response = client.post(
        "/orders",
        json={"products": [{"product_id": product1.id, "quantity": 0}]},
    )

    assert response.status_code == 400
    assert response.json["error"] == "Quantity cannot be less than 1."


def test_order_insufficient_stock(client):
    ingredient1 = Ingredient(
        name="Beef", stock=0.1, initial_stock=0.1
    )  # Only 100g in stock
    product1 = Product(name="Burger")

    db.session.add_all([ingredient1, product1])
    db.session.commit()
    db.session.add(
        ProductIngredient(
            product_id=product1.id, ingredient_id=ingredient1.id, amount=0.15
        )
    )
    db.session.commit()

    response = client.post(
        "/orders",
        json={
            "products": [
                {
                    "product_id": product1.id,
                    "quantity": 2,  # Ordering 2 Burgers (requires 300g of beef)
                }
            ]
        },
    )

    assert response.status_code == 400
    assert response.json["error"] == "Insufficient stock for ingredient Beef."
