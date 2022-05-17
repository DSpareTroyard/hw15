DROP TABLE animal_types;
DROP TABLE breeds;
DROP TABLE outcome_types;
DROP TABLE outcome_subtypes;
DROP TABLE colors;
DROP TABLE animals;
DROP TABLE animals_colors;


CREATE TABLE animal_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE breeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100)
);

CREATE TABLE outcome_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100)
);

CREATE TABLE outcome_subtypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100)
);

CREATE TABLE colors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100)
);

CREATE TABLE animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id varchar(100),
    type_id INTEGER,
    age_upon_outcome varchar(100),
    name varchar(100),
    breed_id INTEGER,
    date_of_birth DATE,
    outcome_subtype_id INTEGER,
    outcome_type_id INTEGER,
    outcome_month INTEGER,
    outcome_year INTEGER,
    FOREIGN KEY (type_id) REFERENCES animal_types(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (breed_id) REFERENCES breeds(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (outcome_subtype_id) REFERENCES outcome_subtypes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (outcome_type_id) REFERENCES outcome_types(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE animals_colors (
    animal_id INTEGER,
    color_id INTEGER,
    FOREIGN KEY (animal_id) REFERENCES animals(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (color_id) REFERENCES colors(id) ON DELETE RESTRICT ON UPDATE CASCADE
);