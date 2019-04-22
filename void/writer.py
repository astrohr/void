def create_table(cursor):
    cursor.execute(
        'CREATE TABLE OBSERVATIONS '
        '(ID INTEGER PRIMARY KEY NOT NULL, '
        'DATE_OBS TIMESTAMP NOT NULL'
        'PATH TEXT NOT NULL, '
        'EXP FLOAT NOT NULL, '
        'OBSERVER TEXT, '
        'POLYGON GEOMETRY NOT NULL);'
    )