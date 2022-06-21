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
);

drop table if exists piece_units cascade;
create table piece_units (
    unit text
);

drop table if exists convert_mass_to_kg cascade;
create table convert_mass_to_kg (
    unit text,
    factor numeric
);

drop table if exists convert_volume_to_l cascade;
create table convert_volume_to_l (
    unit text,
    factor numeric
);