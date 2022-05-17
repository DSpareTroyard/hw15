from utils import clear_tables, get_subtables_data, fulfill_tables, put_data_to_new_db


# удаляет все таблицы и создает их заново
def transfer_data():
    clear_tables()
    tables_strings = get_subtables_data()
    tables = ["animal_types", "colors", "breeds", "outcome_subtypes", "outcome_types"]
    fulfill_tables(tables_strings, tables)
    put_data_to_new_db()


transfer_data()
