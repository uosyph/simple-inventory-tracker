<a name="readme-top"></a>

# Simple Inventory Tracker

This is a Flask-based backend application designed to track products, ingredients, and orders.

The app automatically updates stock levels for ingredients and sends low-stock alerts via email when certain ingredients fall below 50% of their initial stock.

## Table of Contents

-   [Installation](#installation)
-   [Testing](#testing)
-   [Endpoints](#endpoints)
-   [Tech Stack](#tech-stack)
-   [Author](#author)

## Installation

Before you start make sure you have `Python 3.x` installed.

1. **Clone the repository:**

    ```sh
    git clone https://github.com/uosyph/simple-inventory-tracker.git
    cd simple-inventory-tracker
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Add environment variables:**

    Create a `.env` file in the root directory with the following variables:

    ```
    SECRET_KEY=your-secret-key
    DATABASE_URI=postgresql://user:password@host:port/database
    SMTP_SERVER=smtp.example.com
    SMTP_PORT=587
    EMAIL=your-email@example.com
    PASSWORD=your-password
    SENDER=your-email@example.com
    DESTINATION=recipient@example.com
    ```

5. **Run the application**

    ```sh
    python app.py
    ```

    The app will be running on `http://127.0.0.1:5000/`

## Testing

There are unit tests for all functionality in the app, including email sending and order processing.

To run the tests, use the following command:

```sh
pytest tests
```

## Endpoints

### POST `/orders`

Place a new order.

-   **Request:**

    ```json
    {
      "products": [
        {
          "product_id": int,  // ID of the product to order
          "quantity": int     // Number of items to order, must be > 0, defaults to 1 if missing
        }
      ]
    }
    ```

-   **Response:**
    -   `201 Created`: Order placed successfully.
    -   `400 Bad Request`: Invalid quantity, insufficient stock, or missing/invalid data.
    -   `404 Not Found`: Product with specified ID doesn't exist.
    -   `500 Internal Server Error`: Database or other server error.

## Tech Stack

-   **Python**
-   **Flask**
-   **SQLAlchemy**
-   **PostgreSQL**

## Author

**Yousef Saeed**:
[GitHub](https://github.com/uosyph)
[LinkedIn](https://linkedin.com/in/uosyph)
[X](https://twitter.com/uosyph)

<p align="right"><a href="#readme-top">Back to Top</a></p>
