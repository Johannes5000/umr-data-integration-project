drop table if exists recipes cascade;
drop table if exists ingredients cascade;
drop table if exists products cascade;

create table products (
	id int primary key,
	product_name text,
	brand text,
	current_retail_price numeric not null,
	currency text not null,
	number_of_items int not null,
	amount numeric,
	unit text,
	base_price numeric,
	base_unit text
);

create table recipes (
	recipe_id Bigint primary key,
	recipe_name text not null, 
	category text
);

create table ingredients (
	recipe_id Bigint references recipes(recipe_id),
	ingredient_name text not null,
	amount numeric,
	unit text,
	comment text,
	constraint pk primary key (recipe_id, ingredient_name)
);