import psycopg2
import random
import re

type_of_payment = ['Credit', 'Debit', 'Cash']
type_of_store = ["appearlstore", "hardwarestore", "grocerystore"]

def columns_to_string(array):
    #build string through seperator
    seperator = ', '
    return '({str})'.format(str=seperator.join(array))

def fill_tables(cursor, connection, table_name):
    # fill the table if it is empty
    sql_query = 'SELECT count(*) FROM {name}'.format(name=table_name)
    cursor.execute(sql_query)
    number_rows = cursor.fetchone()[0]
    if number_rows >= 10000:
        print('Table full, returning')
        return
    #beginning the build cycle. Must find all columns to fill.
    print('Building table!')
    sql_query = 'SELECT column_name, column_default, is_nullable FROM information_schema.columns WHERE table_name=\'{name}\''.format(name=table_name)
    cursor.execute(sql_query)
    columns = cursor.fetchall()
    column_names = [x[0] for x in columns if (x[1] is None or not re.search('^nextval(.*)$', x[1]))]
    #build string of rows and fill them
    column_names = columns_to_string(column_names)
    sql_insert_base = 'INSERT INTO {table_name} {column_names} VALUES'.format(table_name=table_name, column_names=column_names)
    for _ in range(number_rows,10000):
        rfloat = random.random()
        pick_id = 1+int(rfloat*1000)
        choice = random.choice(type_of_payment)
        amount = round(random.random()*1250, 2)
        
        sql_insert_query = sql_insert_base + ' {values}'.format(values=(pick_id, amount, choice))
        cursor.execute(sql_insert_query)
    # committing the changes to the database 
    connection.commit()


if __name__=="__main__":
    try:
        connection = psycopg2.connect(user = "postgres",
                                  password = "Arya5214",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "test")
        cursor = connection.cursor()

        print("printing number of rows")
        for str in type_of_store:
            fill_tables(cursor, connection, str)
    except (psycopg2.DatabaseError) as error :
        print ("Error while accessing PostgreSQL table.", error)
    except Exception as error:
        print ("Error not purtaining to table access.", error)
    finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")