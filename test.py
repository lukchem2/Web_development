from sqlalchemy import create_engine, MetaData, select

# Step 1: Create engine to connect to SQLite database
engine = create_engine('sqlite:///instance/cafes.db')


# Step 2: Connect to the database
connection = engine.connect()

# Step 3: Reflect the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)
print("------------------------------------")
print(metadata.tables.keys())
print("-----------------------------------------")

# Step 4: Choose a table (e.g., 'users') and query data
users_table = metadata.tables['cafe']

# Step 5: Select all records from the table
query = select(users_table)

# Step 6: Execute the query
result = connection.execute(query)

# Step 7: Fetch and print all rows
for row in result.fetchall():
    print(row)

# Close the connection
connection.close()
