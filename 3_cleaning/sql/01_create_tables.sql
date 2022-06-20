create or replace view view_cleaned_data as (
    select *
    from view_integrated_data
    where ingredient_name not like '%Wasser%' 
        and ingredient_name not like '%wasser%' 
        and ingredient_unit not like 'n. B.' 
        and ingredient_recipe_id not in (
            select distinct ingredient_recipe_id 
            from view_integrated_data
            where first_token_similarity <= 0.9078
        )
)