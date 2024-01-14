CREATE DATABASE IF NOT EXISTS petlebi;
USE petlebi;
CREATE TABLE IF NOT EXISTS petlebi (
    product_id INT NOT NULL,
    product_url VARCHAR(255) NOT NULL,
    product_barcode VARCHAR(50),
    product_name VARCHAR(255) NOT NULL,
    product_price VARCHAR(100),
    product_stock INT NOT NULL,
    product_image VARCHAR(255),
    product_description TEXT,
    product_category VARCHAR(100),
    product_sku VARCHAR(50),
    product_brand VARCHAR(100)
);