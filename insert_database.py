import json, sys, os
from psycopg2 import connect, Error
# import the JSON library from psycopg2.extras
from psycopg2.extras import Json

# import psycopg2's 'json' using an alias
from psycopg2 import extras
from psycopg2.extras import json as psycop_json

# reference : https://kb.objectrocket.com/postgresql/insert-json-data-into-postgresql-using-python-part-2-1248

def load_data_into_database():
    ''' Read json data, and load into a pre-created Postgresql table
    '''
    with open(os.path.join('parsed_json','items_list.json')) as json_data:
        record_list = json.load(json_data)



    if type(record_list) == list :
        first_record = record_list[0]
        columns = list(first_record.keys())
        print("\ncolumn name: ", columns )
        
    # create a nested list of the records' values
    values = [list(x.values()) for x in record_list]

    # value string for the SQL string
    # postgres understand execute_values with list[tuple] [(1,2,3),(4,5,6)]
    values_str = ""
    val_list = []

    # enumerate over the records' values
    for i, record in enumerate(values):

        # declare empty list for values
        # temporarily use list because need to append modified str elements to it
        record_tuple = []
    
        # append each value to a new list of values
        for v, val in enumerate(record):
            if type(val) == str:
                # converting to meet postgres-compliant format
                val = str(Json(val)).replace('"', '')
            record_tuple += [ str(val) ]
        # convert back to tuple
        record_tuple = tuple(record_tuple)
        
        # add to list of value to insert to table
        val_list.append(record_tuple)

    # remove the last comma and end SQL with a semicolon
    values_str = values_str[:-2] + ";"

    
    # Have to create a table in database with matching name
    table_name = 'webscrape_data_happycow' 
    columns_list = ', '.join(columns)

    # concatenate an SQL string
    sql_string = f"INSERT INTO {table_name} ({columns_list})\nVALUES %s" 

    print ("\nSQL string:")
    print (sql_string)

    # establish connection to postgres

    try:
        # declare a new PostgreSQL connection object
        conn = connect(
            dbname = "postgres",
            user = "postgres",
            host = "localhost",
            password = "1",
            # attempt to connect for 3 seconds then raise exception
            connect_timeout = 3
        )

        cur = conn.cursor()
        print ("\ncreated cursor object:", cur)

    except (Exception, Error) as err:
        print ("\npsycopg2 connect error:", err)
        conn = None
        cur = None

    # only attempt to execute SQL if cursor is valid
    if cur != None:

        try:
            extras.execute_values(cur,sql_string,val_list)
            conn.commit()

            print ('\nfinished INSERT INTO execution')

        except (Exception, Error) as error:
            print("\nexecute_sql() error:", error)
            conn.rollback()

        # close the cursor and connection
        cur.close()
        conn.close()

if __name__ == '__main__':
    load_data_into_database()