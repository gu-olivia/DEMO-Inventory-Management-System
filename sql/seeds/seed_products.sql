INSERT INTO products (
    product_name,
    ab_name,
    fluorophore_id,
    part_number,
    host_isotype_name,
    clone_name,
    product_category,
    top_products
)
VALUES
(
    'CD4 APC',
    'CD4',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'APC'),
    '11204P',
    'IgG1,k',
    'SK3',
    'conjugated_ab',
    TRUE
),
(
    'CD4 APC',
    'CD4',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'APC'),
    '10044P',
    'IgG2b, k',
    'OKT4',
    'conjugated_ab',
    TRUE
),
(
    'Kappa FITC',
    'Kappa',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'FITC'),
    '10481P',
    'IgG1,k',
    'TB28-2',
    'conjugated_ab',
    TRUE
),
(
    'Lambda PE',
    'Lambda',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'PE'),
    '10662P',
    'IgG2a, k',
    'HP6054',
    'conjugated_ab',
    TRUE
),
(
    'CD45 mFluor450',
    'CD45',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'mFluor450'),
    '101616P',
    'IgG2a, k',
    'F10-89-4',
    'conjugated_ab',
    TRUE
),
(
    'FLAER iFluor488',
    'FLAER',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'iFluor488'),
    '310511P',
    NULL,
    NULL,
    'conjugated_ab',
    TRUE
),
(
    'CD45 PerCP',
    'CD45',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'PerCP'),
    '10163P',
    'IgG2a, k',
    'F10-89-4',
    'conjugated_ab',
    TRUE
),
(
    'CD3 FITC',
    'CD3',
    (SELECT fluorophore_id FROM fluorophores WHERE fluorophore_name = 'FITC'),
    '10531P',
    'IgG1, k',
    'UCHT1',
    'conjugated_ab',
    TRUE
),
(
    '7-AAD CVSS',
    NULL,
    NULL,
    '3103P',
    NULL,
    NULL,
    'reagent',
    FALSE
),
(
    'RBC Lysis Buffer',
    NULL,
    NULL,
    '310115',
    NULL,
    NULL,
    'reagent',
    FALSE
),
(
    'anti-p53',
    'anti-p53',
    NULL,
    '10220P',
    'IgG1, k',
    'PAB1620',
    'purified_ab',
    FALSE
),
(
    'CD71',
    'CD71',
    NULL,
    '10310P',
    'IgG1, k',
    'OKT9',
    'purified_ab',
    FALSE
),
(
    'CD59',
    'CD59',
    NULL,
    '10420P',
    'IgG1, k',
    'BRA-10G',
    'purified_ab',
    FALSE
);
