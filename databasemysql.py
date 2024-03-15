import mysql.connector
import hashlib



# Constants
SALT = "PasswordSalt"  # Replace this with your actual salt value

# Function to fetch data from the database
def fetch_data(query):
    # Define database connection details
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',  # Update with your password
        'database': 'omr'   # Update with your database name
    }
    
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all rows
        data = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        return data
    except mysql.connector.Error as error:
        print("Error fetching data from MySQL database:", error)
        return None

# DATABASE CONNECTION
def connectToDb():
    host = "localhost"
    user = "root"
    dbPass = ""
    database = "omr"

    try:
        # Connect to the MySQL server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=dbPass,
            database=database
        )

        if connection.is_connected():
            print("Connected to the MySQL database")
            return connection

    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None


# Establish connection to the first database
connection = connectToDb()


def fetch_data_from_database():
    try:
        # Connect to your MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='omr'
        )

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Execute a query to fetch data
        query = "SELECT answerKey FROM operations"
        cursor.execute(query)

        # Fetch all rows from the result set
        data = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        return data

    except mysql.connector.Error as error:
        print("Error fetching data from MySQL database:", error)
        return None


def connectToDb2():
    host = "localhost"
    user = "root"
    dbPass = ""
    database = "elearning"

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=dbPass,
            database=database
        )

        if connection.is_connected():
            print("Connected to the MySQL 2nd database")
            return connection

    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

# Establish connection to the second database
connection2 = connectToDb2()

## USERS

def hash_password(password):
    salted_password = password + SALT
    hashed_password = hashlib.md5(salted_password.encode()).hexdigest()
    return hashed_password

def createUsersTable(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                name TEXT,
                surname TEXT,
                email TEXT NOT NULL,
                password TEXT
            )
        """)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error:", err)
    else:
        return connection


def initializeUsersTable():
    connection = connectToDb()
    if connection:
        cursor = connection.cursor()
        createUsersTable(connection)
        return connection, cursor
    else:
        print("Failed to initialize users table.")
        return None, None


def register(name, surname, email, password):
    con, cursor = initializeUsersTable()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (name, surname, email, password) VALUES (%s, %s, %s, %s)",
                       (name, surname, email, hashed_password))
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Check if the error is due to a duplicate key
            print("Error: Email already exists.")
        else:
            print("Error:", err)
        return False
    else:
        con.commit()
        con.close()
        return True

def login(email, password):
    con, cursor = initializeUsersTable()
    try:
        cursor.execute(
            "SELECT email, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and user[1] == hash_password(password):
            return True
        return False
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        con.close()

def getUserByEmail(email):
    con, cursor = initializeUsersTable()
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not user:
            return None
        else:
            return user


def deleteUserByEmail(email):
    con, cursor = initializeUsersTable()
    try:
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        con.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        con.close()



## OPERATION

def createOperationsTable(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS operations(id TEXT NOT NULL, email TEXT, answerKey TEXT, PRIMARY KEY (id(255)))")
        connection.commit()
        cursor.close()
        print("Operations table created successfully")
    except mysql.connector.Error as err:
        print("Error creating operations table:", err)
    else:
        return connection


def initializeOperationsTable():
    connection = connectToDb()
    if connection:
        cursor = connection.cursor()
        createOperationsTable(connection)
        return connection, cursor
    else:
        print("Failed to initialize operations table.")
        return None, None


def getOperationsByEmail(email):
    con, cursor = initializeOperationsTable()
    try:
        cursor.execute("SELECT * FROM operations WHERE email = %s", (email,))
        operations = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not operations:
            return None
        else:
            operations.reverse()
            return operations



def addOperation(id, email, answerKey):
    con, cursor = initializeOperationsTable()
    id = id.split('uploads/')[1]
    try:
        cursor.execute("INSERT INTO operations (id, email, answerKey) VALUES (%s, %s, %s)",
                       (id, email, answerKey))
        con.commit()
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Check if the error is due to a duplicate key
            print("Error: ID already exists.")
        else:
            print("Error:", err)
        return False
    finally: 
        con.close()
        return True


def getOperationById(id):
    con, cursor = initializeOperationsTable()
    try:
        cursor.execute("SELECT * FROM operations WHERE id = %s", (id,))
        record = cursor.fetchone()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not record:
            return None
        else:
            return record


def deleteOperation(id):
    con, cursor = initializeOperationsTable()
    try:
        cursor.execute("DELETE FROM operations WHERE id = %s", (id,))
        con.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        con.close()
        return True


##  RECORDS

def createRecordsTable(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS records(id TEXT, nameImage TEXT, correct INT, wrong INT, empty INT, score REAL, answers TEXT, image TEXT)")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print("Error:", err)
    else:
        return connection


def initializeRecordsTable():
    connection = connectToDb()
    if connection:
        cursor = connection.cursor()
        createRecordsTable(connection)
        return connection, cursor
    else:
        print("Failed to initialize records table.")
        return None, None


def getRecordsById(id):
    con, cursor = initializeRecordsTable()
    try:
        cursor.execute("SELECT * FROM records WHERE id = %s", (id,))
        records = cursor.fetchall()
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
    else:
        con.close()
        if not records:
            return None
        else:
            return records

def addRecord(id, nameImage, correct, wrong, empty, score, answer, image):
    con, cursor = initializeRecordsTable()
    id = id.split('uploads/')[1]
    try:
        cursor.execute("INSERT INTO records (id, nameImage, correct, wrong, empty, score, answers, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (id, nameImage, correct, wrong, empty, score, answer, image))
        con.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    else:
        con.close()
        return True
# In databasemysql.py
import mysql.connector

def delete_table():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='omr'
        )
        
        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Define the SQL query to drop the table
        drop_query = "DROP TABLE IF EXISTS records"
        
        # Execute the SQL query to drop the table
        cursor.execute(drop_query)
        
        # Commit the changes to the database
        connection.commit()
        
        # Close the cursor and connection
        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as error:
        print("Error deleting table from the database:", error)
        return False






# Example usage:

# if connection:
#     # Do something with the connection
#     pass
# else:
#     print("Failed to connect to the database.")
