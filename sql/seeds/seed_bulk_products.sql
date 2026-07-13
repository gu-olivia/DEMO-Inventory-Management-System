INSERT INTO bulk_products (
    lot_id,
    product_id,
    clone_name,
    lot_number,
    buffer,
    storage_concentration_ug_mL,
    current_volume_mL,
    location,
    remarks
)
VALUES
(1, 1, 'SK3', '4AA3',
'Storage Buffer B', 50, 0.35, 'G37', NULL),

(2, 2, 'OKT4', '120AA6',
'Storage Buffer B', 150, 0.8, 'G60', NULL),

(3, 2, 'OKT4', '120AA8',
'Storage Buffer B', 25, 2.45, 'G67', NULL),

(4, 3, 'TB28-2', '48AF18a',
'Storage Buffer B', 200, 6.75, 'D51', NULL),

(5, 3, 'TB28-2', '48AF20',
'Storage Buffer B', 100, 15.2, 'G33', NULL),

(6, 4, 'HP6054', '66AE13',
'Storage Buffer B', 100, 28.5, 'R41', NULL),

(7, 5, 'F10-89-4', '16A5F32',
'Storage Buffer B', 100, 28.5, 'G66', NULL),

(8, 6, NULL, '310511-38',
'Storage Buffer B', 240, 47.25, 'D65', NULL),

(9, 7, 'F10-89-4', '16AC12a',
'Storage Buffer B', 100, 73.8, 'D41', NULL),

(10, 7, 'F10-89-4', '16AC13',
'Storage Buffer B', 100, 105.5, 'G31', NULL),

(11, 8, 'UCHT1', '53AF40',
'Storage Buffer B', 200, 128.25, 'D65', NULL),

(12, 9, NULL, '3103-10',
'Storage Buffer A', 25, 185, 'G45', NULL),

(13, 10, 'PAB1620', '22AU5',
'PBS 0.1%BSA, 0.09%NaN3', 500, 260.75, 'G34', NULL);
