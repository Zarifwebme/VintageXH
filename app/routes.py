import base64
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from .models import db, Product, User, Cart
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'bmp', 'ico', 'tiff', 'psd', 'raw', 'heif', 'indd'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/')
def home():
    return render_template('admin.html')

@bp.route('/admin2.html')
def admin2():
    return render_template('admin2.html')

# User registration route
@bp.route('/register', methods=['POST'])
def register():
    try:
        firstname = request.form.get('firstname')
        phonenumber = request.form.get('phonenumber')
        password = request.form.get('password')

        if not firstname or not phonenumber or not password:
            return jsonify({"error": "All fields are required."}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(firstname=firstname, phonenumber=phonenumber, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# User login route
@bp.route('/login', methods=['POST'])
def login():
    try:
        phonenumber = request.form.get('phonenumber')
        password = request.form.get('password')

        if not phonenumber or not password:
            return jsonify({"error": "All fields are required."}), 400

        user = User.query.filter_by(phonenumber=phonenumber).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid phone number or password."}), 401

        login_user(user)  # Log in the user
        return redirect(url_for('main.account'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/account')
@login_required
def account():
    try:
        user = current_user
        products = Product.query.all()

        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "classification": product.classification,
                "picture": f"data:{product.mimetype};base64,{base64.b64encode(product.picture).decode('utf-8')}"
            } for product in products
        ]

        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "phonenumber": user.phonenumber
        }

        return jsonify({"user": user_data, "products": product_list}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred", "message": str(e)}), 500

@bp.route('/get_profile', methods=['GET'])
@login_required
def get_profile():
    """Foydalanuvchining profilini olish."""
    try:
        user = current_user
        profile_data = {
            "id": user.id,
            "firstname": user.firstname,
            "phonenumber": user.phonenumber
        }
        return jsonify(profile_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/update_profile', methods=['PUT'])
@login_required
def update_profile():
    """Foydalanuvchining profilini yangilash."""
    try:
        firstname = request.form.get('firstname')
        phonenumber = request.form.get('phonenumber')
        password = request.form.get('password')

        if firstname:
            current_user.firstname = firstname
        if phonenumber:
            current_user.phonenumber = phonenumber
        if password:
            current_user.password = generate_password_hash(password, method='pbkdf2:sha256')

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    """Foydalanuvchining cartiga product qo'shish."""
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity', 1)

        if not product_id:
            return jsonify({"error": "Product ID is required"}), 400

        product = Product.query.get_or_404(product_id)
        existing_cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product.id).first()

        if existing_cart_item:
            existing_cart_item.quantity += int(quantity)
        else:
            cart_item = Cart(user_id=current_user.id, product_id=product.id, quantity=int(quantity))
            db.session.add(cart_item)

        db.session.commit()
        return jsonify({"message": "Product added to cart successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/get_cart', methods=['GET'])
@login_required
def get_cart():
    """Foydalanuvchining cartini olish."""
    try:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        cart_list = [
            {
                "product_id": item.product_id,
                "name": item.product.name,
                "price": item.product.price,
                "classification": item.product.classification,
                "quantity": item.quantity,
                "picture": f"data:{item.product.mimetype};base64,{base64.b64encode(item.product.picture).decode('utf-8')}"
            } for item in cart_items
        ]
        return jsonify(cart_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@bp.route('/get_users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        user_list = [
            {
                "id": user.id,
                "firstname": user.firstname,
                "phonenumber": user.phonenumber
            } for user in users
        ]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/get_user_count', methods=['GET'])
def get_user_count():
    try:
        count = User.query.count()
        return jsonify({"count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/add_product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    classification = request.form.get('classification')
    picture = request.files.get('picture')

    if not name or not price or not classification or not picture:
        return jsonify({"error": "All fields are required."}), 400

    try:
        price = float(price)
    except ValueError:
        return jsonify({"error": "Invalid price format."}), 400

    if allowed_file(picture.filename):
        mimetype = picture.mimetype
        picture_data = picture.read()

        new_product = Product(name=name, price=price, classification=classification,
                              picture=picture_data, mimetype=mimetype)

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully!"}), 201
    else:
        return jsonify({"error": "Unsupported image format"}), 400


@bp.route('/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "classification": product.classification,
            "picture": f"data:{product.mimetype};base64,{base64.b64encode(product.picture).decode('utf-8')}"
        } for product in products
    ]
    return jsonify(product_list), 200


@bp.route('/get_product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "classification": product.classification,
            "picture": f"data:{product.mimetype};base64,{base64.b64encode(product.picture).decode('utf-8')}"
        }
        return jsonify(product_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/update_product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    name = request.form.get('name')
    price = request.form.get('price')
    classification = request.form.get('classification')
    picture = request.files.get('picture')

    if name:
        product.name = name
    if price:
        try:
            product.price = float(price)
        except ValueError:
            return jsonify({"error": "Invalid price format"}), 400
    if classification:
        product.classification = classification
    if picture and allowed_file(picture.filename):
        product.picture = picture.read()
        product.mimetype = picture.mimetype

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200


@bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200


@bp.route('/search_products', methods=['GET'])
def search_products():
    query = request.args.get('query')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    product_list = [
        {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "classification": product.classification,
            "picture": f"data:{product.mimetype};base64,{base64.b64encode(product.picture).decode('utf-8')}"
        } for product in products
    ]
    return jsonify(product_list), 200

@bp.route('/get_product_count', methods=['GET'])
def get_product_count():
    try:
        count = Product.query.count()
        return jsonify({"count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
