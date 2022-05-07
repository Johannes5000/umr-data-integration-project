create table products (
	id int primary key,
	productName text,
	brand text,
	currentRetailPrice numeric not null,
	currency text not null,
	grammage text,
	basePrice numeric,
	baseUnit text
);