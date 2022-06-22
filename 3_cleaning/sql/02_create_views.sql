create or replace view view_integrated_data as (
    select I.*, P.*, M.similarity, M.first_token_similarity
    from view_renamed_ingredients I
    join ingredients_with_rewe_products M on (
        I.ingredient_name = M.ingredient_name and 
        ((I.ingredient_unit = M.ingredient_unit ) or (I.ingredient_unit is null and M.ingredient_unit is null))
    )
    join view_cleaned_products P on (
        P.product_name = M.product_name and 
        ((P.product_unit = M.product_unit ) or (P.product_unit is null and M.product_unit is null))
    )
);