drop view if exists view_showcase_ingredients_with_price;
create view view_showcase_ingredients_with_price as (
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
    ), case_one_pieces_data as (
        select *
        from filtered_showcase_data
        where ingredient_unit in (select * from piece_units)
    ), data_without_case_one as (
        (select * from filtered_showcase_data)
        except
        (select * from case_one_pieces_data)
    ), case_two_volume_data as (
        select *
        from data_without_case_one
        where ingredient_unit in (select unit from convert_volume_to_l)
            and product_unit in ('L', 'ML')
    ), data_without_case_one_two as (
        (select * from data_without_case_one)
        except
        (select * from case_two_volume_data)
    ), case_three_mass_data as (
        select *
        from data_without_case_one_two
        where ingredient_unit in (select unit from convert_mass_to_kg)
            and product_unit in ('G', 'KG')
    ), case_four_rest_data as (
        (select * from data_without_case_one_two)
        except
        (select * from case_three_mass_data)
    ), calculate_case_one_pieces_data as (
        select *, ingredient_amount * product_current_retail_price as ingredient_price
        from case_one_pieces_data
    ), calculate_case_two_volume_data as (
        select D.*, (D.ingredient_amount * IC.factor) / (PC.factor * COALESCE(D.product_amount, 1)) * D.product_current_retail_price as ingredient_price
        from case_two_volume_data D
            join convert_volume_to_l IC on D.ingredient_unit = IC.unit
            join convert_volume_to_l PC on D.product_unit = PC.unit
    ), calculate_case_three_mass_data as (
        select D.*, (D.ingredient_amount * IC.factor) / (PC.factor * COALESCE(D.product_amount, 1)) * D.product_current_retail_price as ingredient_price
        from case_three_mass_data D
            join convert_mass_to_kg IC on D.ingredient_unit = IC.unit
            join convert_mass_to_kg PC on D.product_unit = PC.unit
    ), calculate_case_four_rest_data as (
        select *, product_current_retail_price as ingredient_price
        from case_four_rest_data
    ), combined_data_with_price as (
        (select * from calculate_case_one_pieces_data)
        union
        (select * from calculate_case_two_volume_data)
        union
        (select * from calculate_case_three_mass_data)
        union
        (select * from calculate_case_four_rest_data)
    )
    select * from combined_data_with_price
);

drop view if exists view_showcase_recipes_price;
create view view_showcase_recipes_price as (
    with aggregates as (
        select ingredient_recipe_id as recipe_id, sum(ingredient_price) as recipe_price, 
            avg(similarity) as avg_sim, avg(first_token_similarity) as avg_first_token_sim
        from view_showcase_ingredients_with_price
        group by ingredient_recipe_id
    )
    select *
    from recipes natural join aggregates
);