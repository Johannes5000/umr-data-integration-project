create or replace view view_cleaned_products as (
    with duplicate_product_list as (
        select product_name, max(product_id) as newest_id
        from view_renamed_products
        group by product_name
        having count(*) > 1
    ),
    single_cleaned_products as (
        select * 
        from view_renamed_products
        where product_name not in (select product_name from duplicate_product_list)
    ),
    duplicate_cleaned_products as (
        select *
        from view_renamed_products P 
        where exists (
            select * 
            from duplicate_product_list D
            where P.product_name = D.product_name
                and P.product_id = D.newest_id
        )
    )
    (select * from single_cleaned_products)
    union
    (select * from duplicate_cleaned_products)
);