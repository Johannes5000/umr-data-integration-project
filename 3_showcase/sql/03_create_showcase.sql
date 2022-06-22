drop view if exists view_showcase;
create view view_showcase as (
    with ignore_water as (
        select *
        from view_integrated_data
        where ingredient_name not like 'Wasser%' 
            and ingredient_name not like 'wasser%'
    ), filter_units_to_ignore as (
        select *
        from ignore_water
        where ingredient_unit not in (select * from units_to_ignore)
    ), recipe_ids_to_ignore as (
        select distinct ingredient_recipe_id as recipe_id
        from filter_units_to_ignore
        where first_token_similarity < 0.9078
        order by ingredient_recipe_id
    ), filtered_showcase_data as (
        select *
        from filter_units_to_ignore
        where ingredient_recipe_id not in (select * from recipe_ids_to_ignore)
    )
    select * from filtered_showcase_data
);