-- Stores packaged products that are ready to ship out
CREATE TABLE packaged_products (
    packaged_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    lot_id INT NOT NULL,              -- reference to lot
    product_id INT NOT NULL,          -- reference to product
    clone_name VARCHAR(50),           -- optional, mostly matches lot
    unit_price DECIMAL(10,2),
    packaging_date DATE,
    packaging_concentration_ug_mL DECIMAL(10,2),
    qty_remaining INT CHECK (qty_remaining >= 0),
    product_catalog_number VARCHAR(50),
    size VARCHAR(50),
    location VARCHAR(50),
    buffer VARCHAR(50),
    cost_of_goods DECIMAL(10,2),
    remarks VARCHAR(50),

    CONSTRAINT fk_packaged_lot
        FOREIGN KEY (lot_id)
        REFERENCES lots(lot_id),

    CONSTRAINT fk_packaged_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
