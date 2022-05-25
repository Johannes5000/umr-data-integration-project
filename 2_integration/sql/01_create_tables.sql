drop table if exists ingredients_with_rewe_products cascade;

create table ingredients_with_rewe_products (
    ingredient_name text,
    ingredient_cleaned_name text,
    ingredient_unit text,
    product_name text,
    product_cleaned_name text,
    product_unit text,
    similarity numeric,
    first_token_similarity numeric
);