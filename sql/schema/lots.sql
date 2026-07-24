-- Describes attributes that are specific to one lot.
-- Bulk and packaged specifications are stored in their respective tables.
CREATE TABLE lots (
    lot_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INT NOT NULL,
    clone_name VARCHAR(50),
    lot_number VARCHAR(50),
    creation_date DATE,
    expiration_date DATE,
    product_state VARCHAR(50), -- e.g. Active or DQ'd
    test_5ul_concentration_ug_ml DECIMAL(10,2) NOT NULL,
    initial_volume_mL DECIMAL(10,2) NOT NULL,
    remarks VARCHAR(50),

    CONSTRAINT fk_lot_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
