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

create or replace view view_renamed_products as (
    select
        id as product_id,
        product_name as product_name,
        brand as product_brand,
        current_retail_price as product_current_retail_price,
        currency as product_currency,
        number_of_items as product_number_of_items,
        amount as product_amount,
        unit as product_unit,
        base_price as product_base_price,
        base_unit as product_base_unit
    from products
);

create or replace view view_renamed_ingredients as (
    select 
        recipe_id as ingredient_recipe_id,
        ingredient_name as ingredient_name,
        amount as ingredient_amount,
        unit as ingredient_unit,
        comment as ingredient_comment
    from ingredients
);