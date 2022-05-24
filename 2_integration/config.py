from configparser import ConfigParser

SQL_CREATE_TABLES_FILEPATH = '2_integration\\sql\\01_create_tables.sql'
INGREDIENTS_PRODUCTS_MAPPING_FILEPATH = '2_integration\\ingredients_products_mapping.json'

INGREDIENT_NAMES_FILEPATH = '2_integration\\ingredient_names.json'
PRODUCT_NAMES_FILEPATH = '2_integration\\product_names.json'


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    c = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            c[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return c