


import sqlite3

"""
componentType
--------------------
- componentTypeID (Primary Key)
- componentType (e.g., Resistor, Capacitor)

manufacturer
------------------
- manufacturerID  (Primary Key)
- manufacturerName (str)

component
---------------
- componentID (Primary Key)
- componentTypeID (Foreign Key to Component Type Table)
- manufacturerID (Foreign Key to Manufacturer Table)
- componentName

componentSpecifications
------------------------------
- specID (Primary Key)
- componentID (Foreign Key to Component Table)
- specName
- specValue
"""

databasePath = "D:/Coding/Projects/SemiConductorGPT/website/instance/database.db"
conn = sqlite3.connect(databasePath)
cursor = conn.cursor()

# Enable foreign key support (needed for some SQLite versions)
#cursor.execute("PRAGMA foreign_keys = ON")


# Insert multiple records using the more secure "?" method
#employees = [('Jane Doe', 'Developer', 80000),
#             ('Mike Smith', 'Designer', 70000),
#             ('Anna Johnson', 'Sales', 65000)]
#cursor.executemany("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)", employees)

#conn.commit()



"""
____________________________ insertIntoTable ____________________________
This function inserts data into the db

table = This is the name of the table you want to insert data into (str)
dataList = This is the data you want to insert data into, (list) FORMAT: [(data1, data2), (data3, data4)]
cursor = This is the cursor used to do commands to the db (obj)
conn = This id the connection to the db, for making read and writes. if not inputted, then there will be done no commits

Returns: None
"""


def insertIntoTable(table, dataList, columnNames, cursor, conn=None):
    sqlCommand = f"INSERT INTO {table}"

    
    if len(dataList[0]) != 0:
        if len(columnNames) != 0: 
            lastIndex = len(columnNames) -1
            sqlCommand = sqlCommand + "("
            for column in columnNames[:lastIndex]:
                sqlCommand = sqlCommand + f"{column}, "

            sqlCommand = sqlCommand + f"{columnNames[lastIndex]}) VALUES ("

        

            for i in range(len(dataList[0]) -1):
                sqlCommand = sqlCommand + "?, "

            sqlCommand += "?)"
            print(sqlCommand)
            cursor.executemany(sqlCommand, dataList)

            if conn != None:
                conn.commit()        
    else:
        raise Exception("Cannot insert into table when there is no data!")


"""
__________________________ deleteRowsFromTable __________________________
This function deletes rows from a table
table = This is the name of the table you want to delete data from (str)
whereStatment = This could forexample be a column name, because you want to delete * where id = 1 (str)
parameter = This is the parameter you want to delete from. example: delete * where id = 1. This is the 1 (str)
cursor = This is the cursor used to do commands to the db (obj)
conn = This id the connection to the db, for making read and writes. if not inputted, then there will be done no commits

Returns: None

"""

def deleteRowsFromTable(table, whereStatment, parameter, cursor, conn=None):
    sqlCommand = f"DELETE FROM {table} WHERE {whereStatment} = '{parameter}'"
    print(sqlCommand)
    cursor.execute(sqlCommand)

    if conn != None:
        conn.commit()

def getDataFromTable(table, columnList, parameterTup, cursor):
    sqlCommand = f"SELECT * FROM {table} WHERE"

    if len(columnList) > 1:
        for i, parameter in enumerate(columnList):
            sqlCommand = sqlCommand + f" {parameter} = ?"

            if i != len(columnList) - 1:
                sqlCommand = sqlCommand + " AND"
    else:
        sqlCommand = sqlCommand + f" {columnList[0]} = '{parameterTup[0]}'"
        cursor.execute(sqlCommand)
        rows = cursor.fetchall()
        return rows
    
    cursor.execute(sqlCommand, parameterTup)
    rows = cursor.fetchall()    
    return rows


    #cursor.execute("'")

    

#deleteRowsFromTable("componentType", "componentType", "ic", cursor, conn=conn)


#insertIntoTable("manufacturer", [("infineon",)], ["manufacturerName"], cursor, conn)

#cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
#print(cursor.fetchall())
#
#cursor.execute("DELETE FROM manufacturer")
#cursor.execute("DELETE FROM component")
#cursor.execute("DELETE FROM componentSpecifications")
#
# Commit the changes
#conn.commit()


#cursor.executemany("INSERT INTO componentType (componentType) VALUES (?)", employees)
#conn.commit()





# Query the database
#cursor.execute("SELECT * FROM employees")
#
## Fetch all rows from the last executed statement
#results = cursor.fetchall()
#
## Display the results
#for row in results:
#    print(row)
#
## Close the connection when done
conn.close()






"""

# Creating the componentType table
cursor.execute('''CREATE TABLE IF NOT EXISTS componentType (
                    componentTypeID INTEGER PRIMARY KEY, 
                    componentType TEXT)''')

# Creating the manufacturerTable
cursor.execute('''CREATE TABLE IF NOT EXISTS manufacturer (
                    manufacturerID INTEGER PRIMARY KEY, 
                    manufacturerName TEXT)''')

# Creating the componentTable
cursor.execute('''CREATE TABLE IF NOT EXISTS component (
                    componentID INTEGER PRIMARY KEY, 
                    componentTypeID INTEGER, 
                    manufacturerID INTEGER,
                    componentName TEXT,
                    FOREIGN KEY(componentTypeID) REFERENCES componentType(componentTypeID),
                    FOREIGN KEY(manufacturerID) REFERENCES manufacturerTable(manufacturerID))''')

# Creating the componentSpecificationsTable
cursor.execute('''CREATE TABLE IF NOT EXISTS componentSpecifications (
                    specID INTEGER PRIMARY KEY, 
                    componentID INTEGER, 
                    specName TEXT,
                    specValue TEXT,
                    FOREIGN KEY(componentID) REFERENCES componentTable(componentID))''')

# Commit and close
conn.commit()
conn.close()

"""