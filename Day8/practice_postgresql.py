import psycopg2

# Establishing the connection
conn = psycopg2.connect(
    database="databasename",
    user='root',
    password='root',
    host='',
    port='5432'
)

# Creating a cursor object using the
# cursor() method
cursor = conn.cursor()

# Doping EMPLOYEE table if already exists.
cursor.execute("DROP TABLE IF EXISTS publisher")

# Creating table as per requirement
sql = '''CREATE TABLE PUBLISHER(
                publisher_id SERIAL PRIMARY KEY,
                publisher_name VARCHAR(255) NOT NULL,
                publisher_estd INT,
                publsiher_location VARCHAR(255),
                publsiher_type VARCHAR(255)
)'''
cursor.execute(sql)
print("Table created successfully........")
conn.commit()

# Closing the connection
conn.close()
