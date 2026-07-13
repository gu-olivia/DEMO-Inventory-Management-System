CREATE TABLE fluorophores (
    fluorophore_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    fluorophore_name VARCHAR(20) NOT NULL,
    fluorophore_group INT,
    display_name VARCHAR(20) NOT NULL
);
