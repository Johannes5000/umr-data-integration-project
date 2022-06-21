drop table if exists showcase;
create table showcase (
		ingredient_recipe_id Bigint,
		ingredient_name text,
		ingredient_amount numeric,
		ingredient_unit text,
		ingredient_comment text,
		product_id int,
		product_name text,
		product_brand text,
		product_current_retail_price numeric,
		product_currency text,
		product_number_of_items int,
		product_amount numeric,
		product_unit text,
		product_base_price numeric,
		product_base_unit text,
		similarity numeric,
		first_token_similarity numeric,
		unit text,
		factor numeric,
		ingredient_base_amount numeric,
		product_base_amount numeric
);

with liquids as (
	select *, ingredient_amount * factor as ingredient_base_amount, product_amount * factor as product_base_amount
	from view_cleaned_data join convert_volume_to_l on view_cleaned_data.ingredient_unit = convert_volume_to_l.unit
	where ingredient_unit in (
		select unit 
		from convert_volume_to_l
	)
)
insert into showcase (select * from liquids);

with mass as (
	select *, ingredient_amount * factor as ingredient_base_amount, product_amount * factor as product_base_amount
	from view_cleaned_data join convert_mass_to_kg on view_cleaned_data.product_base_unit = convert_mass_to_kg.unit
	where product_base_unit in (
		select unit 
		from convert_mass_to_kg
	)
)
insert into showcase (select * from mass);

with pieces as (
	select * 
	from view_cleaned_data
	where ingredient_unit in (
		select unit 
		from piece_units
	)
)
insert into showcase (select * from pieces);

with liquids as (
	select *, ingredient_amount * factor as ingredient_base_amount
	from view_cleaned_data join convert_volume_to_l on view_cleaned_data.ingredient_unit = convert_volume_to_l.unit
	where ingredient_unit in (
		select unit 
		from convert_volume_to_l
	)
)
, mass as (
	select *, ingredient_amount * factor as ingredient_base_amount 
	from view_cleaned_data join convert_mass_to_kg on view_cleaned_data.ingredient_unit = convert_mass_to_kg.unit
	where ingredient_unit in (
		select unit 
		from convert_mass_to_kg
	)
)
, pieces as (
	select * 
	from view_cleaned_data
	where ingredient_unit in (
		select unit 
		from piece_units
	)
)
, rest as (
	select * 
	from view_cleaned_data 
	where ingredient_unit not in (
		select ingredient_unit from liquids 
		union 
		select ingredient_unit from mass 
		union 
		select ingredient_unit from pieces
	)
)
insert into showcase (select * from rest);