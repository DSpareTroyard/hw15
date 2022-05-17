import sqlite3
import datetime


def clear_tables():
    with open("query.sql", "r", encoding='utf-8') as f:
        query = f.read()

    with sqlite3.connect("animals.db") as connection:
        cursor = connection.cursor()
        cursor.executescript(query)


def get_list_from_db(query):
    with sqlite3.connect("animal.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        list_ = []
        for item in result:
            list_.append(str(item[0]).strip())

    return list_


def get_subtables_data():
    select_query = "SELECT DISTINCT animal_type FROM animals"
    animal_types = get_list_from_db(select_query)

    select_query = "SELECT DISTINCT breed FROM animals"
    breed_types = get_list_from_db(select_query)

    select_query = "SELECT DISTINCT color1, color2 FROM animals"
    colors = list(set(get_list_from_db(select_query)))

    select_query = "SELECT DISTINCT outcome_subtype FROM animals"
    outcome_subtypes = get_list_from_db(select_query)

    select_query = "SELECT DISTINCT outcome_type FROM animals"
    outcome_types = get_list_from_db(select_query)

    return [animal_types, colors, breed_types, outcome_subtypes, outcome_types]


def fulfill_tables(tables_strings, tables):
    with sqlite3.connect("animals.db") as connection:
        cursor = connection.cursor()

        for table, table_data in zip(tables, tables_strings):

            insert_query = f"INSERT INTO {table} (`name`) VALUES "
            for item in table_data:
                insert_query += f"('{item.strip()}'), "

            insert_query = insert_query[:len(insert_query) - 2]
            cursor.execute(insert_query)


def get_animals_data(offset=0, limit=10):
    with sqlite3.connect("animal.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT * FROM animals LIMIT {limit} OFFSET {offset}"
        cursor.execute(select_query)
        result = cursor.fetchall()
        field_names = [i[0] for i in cursor.description]
        table_data = []
        for row in result:
            row_data = {}
            for field, cell in zip(field_names, row):
                row_data[field] = cell
            table_data.append(row_data)
    return table_data


def get_animals_count():
    with sqlite3.connect("animal.db") as connection:
        cursor = connection.cursor()
        select_query = "SELECT COUNT(`index`) FROM animals"
        cursor.execute(select_query)
        result = cursor.fetchone()

        return result[0]


def put_data_to_new_db():
    k = 0;
    with sqlite3.connect("animals.db") as connection:
        cursor = connection.cursor()
        animals_count = get_animals_count() // 10 + 1
        for i in range(0, animals_count):
            animals_data = get_animals_data(i * 10)
            insert_query = """
                INSERT INTO animals
                (age_upon_outcome, animal_id, name, date_of_birth, outcome_month, outcome_year)
                VALUES
                """
            for item in animals_data:
                insert_query += f"""
                            (\"{item['age_upon_outcome']}\", \"{item['animal_id']}\",  
                                \"{item['name']}\", \"{item['date_of_birth']}\", 
                                {item['outcome_month']}, {item['outcome_year']}),"""

            insert_query = insert_query[:-1]
            cursor.execute(insert_query)
            for item in animals_data:
                animal_id = item['animal_id'].strip()
                animal_type = item['animal_type'].strip()
                breed = item['breed'].strip()
                outcome_subtype = str(item['outcome_subtype']).strip()
                outcome_type = str(item['outcome_type']).strip()
                color1 = str(item['color1']).strip()
                color2 = str(item['color2']).strip()

                select_query = f"SELECT animal_types.id, breeds.id, " \
                               f"outcome_subtypes.id, outcome_types.id " \
                               f"FROM animal_types, breeds, " \
                               f"outcome_subtypes,  outcome_types " \
                               f"WHERE animal_types.name = '{animal_type}' " \
                               f"AND breeds.name = '{breed}' " \
                               f"AND outcome_subtypes.name = '{outcome_subtype}' " \
                               f"AND outcome_types.name = '{outcome_type}'"
                cursor.execute(select_query)
                result = cursor.fetchone()
                insert_id_query = f"UPDATE animals " \
                                  f"SET type_id = {result[0]}, " \
                                  f"breed_id = {result[1]}, " \
                                  f"outcome_subtype_id = {result[2]}, " \
                                  f"outcome_type_id = {result[3]} " \
                                  f"WHERE animal_id = '{animal_id}'"
                cursor.execute(insert_id_query)

                select_query = f"SELECT animals.id, colors.id FROM colors, animals " \
                               f"WHERE colors.name = '{color1}' " \
                               f"AND animals.animal_id = '{animal_id}'"
                cursor.execute(select_query)
                result = cursor.fetchone()
                insert_id_query = f"INSERT INTO animals_colors (animal_id, color_id) " \
                                  f"VALUES ({result[0]}, {result[1]})"
                cursor.execute(insert_id_query)

                select_query = f"SELECT animals.id, colors.id FROM colors, animals " \
                               f"WHERE colors.name = '{color2}' " \
                               f"AND animals.animal_id = '{animal_id}'"
                cursor.execute(select_query)
                result = cursor.fetchone()
                if result:
                    insert_id_query = f"INSERT INTO animals_colors (animal_id, color_id) " \
                                      f"VALUES ({result[0]}, {result[1]})"
                    cursor.execute(insert_id_query)

                k += 1
                print(f"{k} из {get_animals_count()}")


def get_animal(animal_index):
    with sqlite3.connect("animals.db") as connection:
        cursor = connection.cursor()
        select_query = f"SELECT animals.id, animals.age_upon_outcome as 'age', " \
                       f"animals.name, animals.date_of_birth, animals.animal_id, " \
                       f"animals.outcome_month, animals.outcome_year, " \
                       f"animal_types.name as 'type', " \
                       f"breeds.name as 'breed', " \
                       f"outcome_types.name as 'outcome_type', " \
                       f"outcome_subtypes.name as 'outcome_subtype' " \
                       f"FROM animals " \
                       f"INNER JOIN animal_types ON animals.type_id = animal_types.id " \
                       f"INNER JOIN breeds ON animals.breed_id = breeds.id " \
                       f"INNER JOIN outcome_types ON animals.outcome_type_id = outcome_types.id " \
                       f"INNER JOIN outcome_subtypes ON animals.outcome_subtype_id = outcome_subtypes.id " \
                       f"WHERE animals.id = '{animal_index}'"
        cursor.execute(select_query)
        result = cursor.fetchone()
        field_names = [i[0] for i in cursor.description]
        animal = {}
        for item, field in zip(result, field_names):
            animal[field] = item

        select_query = f"SELECT colors.name " \
                       f"FROM animals_colors " \
                       f"INNER JOIN colors ON colors.id = animals_colors.color_id " \
                       f"WHERE animal_id = {animal_index}"
        cursor.execute(select_query)
        result = cursor.fetchall()
        colors = [i[0] for i in result]
        animal['colors'] = colors
        animal['date_of_birth'] = datetime.datetime.strptime(animal['date_of_birth'], "%Y-%m-%d %H:%M:%S").date()

        return animal
