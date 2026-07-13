CREATE TABLE bulk_products (
    lot_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    clone_name VARCHAR(50),
    lot_number VARCHAR(50),
    buffer VARCHAR(50),
    storage_concentration_ug_mL DECIMAL(10,2) NOT NULL,
    current_volume_mL DECIMAL(10,2) NOT NULL,

    amount_remaining_ug DECIMAL(12,2)
        GENERATED ALWAYS AS (
            storage_concentration_ug_mL * current_volume_mL
        ) STORED,

    location VARCHAR(50),
    remarks VARCHAR(50),

    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (lot_id) REFERENCES lots(lot_id)
);
