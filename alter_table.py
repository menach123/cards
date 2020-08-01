import sqlconnection
conn = sqlconnection.DBManager()

def main():
    # query = "ALTER TABLE hands RENAME TO _old;"

    # conn.query(query)

    # query = "CREATE TABLE hands(cards varchar(255) PRIMARY KEY, prob10 float(3,2))"
    # conn.query(query)

    query = "INSERT INTO hands (cards, prob10) SELECT * FROM _old;)"
    conn.query(query)

    query = "DROP TABLE _old;"
    conn.query(query)
    pass


if __name__ == "__main__":
    main()

print("Guru99")