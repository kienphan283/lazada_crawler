import mysql.connector

mydb = mysql.connector.connect(

    host="localhost",

    user="root",

    database="lazada_db"

)



mycursor = mydb.cursor()



# Tạo bảng customers

mycursor.execute("""

CREATE TABLE customers (

    customer_id INT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(255) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    phone VARCHAR(20),

    address VARCHAR(255),

    password VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

)

""")



# Tạo bảng categories

mycursor.execute("""

CREATE TABLE categories (

    category_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    parent_category_id INT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)

)

""")



# Tạo bảng subcategories

mycursor.execute("""

CREATE TABLE subcategories (

    subcategory_id INT AUTO_INCREMENT PRIMARY KEY,

    category_id INT NOT NULL,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id) REFERENCES categories(category_id)

);

""")        

# Tạo bảng products

mycursor.execute("""

CREATE TABLE products (

    product_id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(255) NOT NULL,

    description TEXT,

    price DECIMAL(10, 2) NOT NULL,

    stock_quantity INT NOT NULL,

    image_url VARCHAR(255),

    category_id INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (category_id) REFERENCES categories(category_id)

)

""")


# Tạo bảng orders

mycursor.execute("""

CREATE TABLE orders (

    order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    order_date DATE NOT NULL,

    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') NOT NULL,

    shipping_address VARCHAR(255) NOT NULL,

    payment_method ENUM('cash', 'credit_card', 'paypal') NOT NULL,

    total_amount DECIMAL(10, 2) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)

)

""")



# Tạo bảng order_items

mycursor.execute("""

CREATE TABLE order_items (

    order_item_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    product_id INT NOT NULL,

    quantity INT NOT NULL,

    price DECIMAL(10, 2) NOT NULL,

    FOREIGN KEY (order_id) REFERENCES orders(order_id),

    FOREIGN KEY (product_id) REFERENCES products(product_id)

)

""")



# Tạo bảng payments

mycursor.execute("""

CREATE TABLE payments (

    payment_id INT AUTO_INCREMENT PRIMARY KEY,

    order_id INT NOT NULL,

    amount DECIMAL(10, 2) NOT NULL,

    payment_method ENUM('cash', 'credit_card', 'paypal') NOT NULL,

    status ENUM('pending', 'paid', 'failed') NOT NULL,

    transaction_id VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (order_id) REFERENCES orders(order_id)

)

""")



# Tạo bảng reviews

mycursor.execute("""

CREATE TABLE reviews (

    review_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    product_id INT NOT NULL,

    rating INT NOT NULL,

    review_content TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),

    FOREIGN KEY (product_id) REFERENCES products(product_id)

)

""")



# Tạo bảng carts

mycursor.execute("""

CREATE TABLE carts (

    cart_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    product_id INT NOT NULL,

    quantity INT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),

    FOREIGN KEY (product_id) REFERENCES products(product_id)

)

""")



# Tạo bảng wishlists

mycursor.execute("""

CREATE TABLE wishlists (

    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    product_id INT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),

    FOREIGN KEY (product_id) REFERENCES products(product_id)

)

""")



# Tạo bảng customer_orders

mycursor.execute("""

CREATE TABLE customer_orders (

    customer_order_id INT AUTO_INCREMENT PRIMARY KEY,

    customer_id INT NOT NULL,

    order_id INT NOT NULL,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),

    FOREIGN KEY (order_id) REFERENCES orders(order_id)

)

""")

# Tạo bảng sub_subcategories
mycursor.execute("""
CREATE TABLE sub_subcategories (
    sub_subcategory_id INT AUTO_INCREMENT PRIMARY KEY,
    subcategory_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT   
 CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,   

    FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id)
);
""")

# Cập nhật bảng products để liên kết với bảng subcategories (nếu chưa có)
mycursor.execute("""
ALTER TABLE products
ADD COLUMN subcategory_id INT,
ADD FOREIGN KEY (subcategory_id) REFERENCES subcategories(subcategory_id);
""")

mydb.commit()
print("Đã tạo bảng thành công")

mydb.close()