drop table if exists ingredients_with_rewe_products cascade;

create table ingredients_with_rewe_products (
    ingredient_name text,
    product_name text,
    constraint pk2 primary key (ingredient_name, product_name)
);