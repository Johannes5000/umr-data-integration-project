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

create table base_units (
    base_unit text primary key,
    amount int not null
);