# vintageXH Explore

## Overview
vintageXH Explore is a web application that allows users to browse and order vintage products. The application provides user registration, login, profile management, product browsing, and ordering functionalities.

## Features
- User Registration and Login
- Profile Management
- Product Browsing
- Add Products to Cart
- View Cart
- Place Orders

## Technologies Used
- Python
- Flask
- SQLAlchemy
- JavaScript
- HTML/CSS
- Bootstrap

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/vintageXH.git
    cd vintageXH
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

5. **Run the application:**
    ```sh
    flask run
    ```

## API Endpoints

### User Endpoints
- **Register a new user:** `POST /register`
- **Login a user:** `POST /login`
- **Get account information:** `GET /account`
- **Update profile information:** `PUT /update_profile`
- **Logout a user:** `POST /logout`

### Product Endpoints
- **Add a new product:** `POST /add_product`
- **Retrieve all products:** `GET /get_products`
- **Update a product:** `PUT /update_product/{product_id}`
- **Delete a product:** `DELETE /delete_product/{product_id}`
- **Search for a product:** `GET /search_product`
- **Get a product:** `GET /get_product/{product_id}`
- **Get the count of products:** `GET /get_product_count`

### Cart Endpoints
- **Add a product to the cart:** `POST /add_to_cart/{product_id}`
- **Get the cart:** `GET /get_cart`

### Order Endpoints
- **Place an order:** `POST /place_order`

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
For any inquiries, please contact [your email address].
