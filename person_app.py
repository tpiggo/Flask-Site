import psycopg2
import re
import datetime

available_tasks = [
    'end', 'nothing', 'request_data', 'show_person_all', 'person_all_stores',
    'available_tasks', 'show_person_short', 'show_person_attribute',
    'show_person_hardware_store', 'show_person_appearl_store', 'show_person_grocery_stores'
    ]
#No other choices since all other attributes of people may be none unique, thus causing problems
choice_of_index = [
    'id', 'full_name', 'email'
]

def parse_input(string:str):
    string = string.replace(' ', '_')
    string = str.lower(string)
    return string

def run():
    end = True
    starttime = datetime.datetime.utcnow
    while end:
        print("Running since", starttime)
        task = input("Give me a task: ")
        task = parse_input(task)
        if task in available_tasks:
            if task=='available_tasks':
                # not a good work around but will have to do for now
                print('Available Tasks are:', available_tasks)
            elif task == 'end':
                print("Shutting down application")
                end=False
            else:
                choice = find_by(task=task)
                
        else:
            print("Task {task}".format(task=task), " was not recognized.")
            

def find_by(task=None):
    choice = input('Select a how you wish to find the data from the following choices,{values}: '.format(values=choice_of_index))
    while (not parse_input(choice) in choice_of_index):
        choice = input('Please select from the choices provided,{values}: '.format(values=choice_of_index))
    return choice


def access_databases():
    try:
        #should really put this into a .env file
        # when you start the cursor, do not forget to close it
        connection = psycopg2.connect(user = "postgres",
                                  password = "Arya5214",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "test")
       

    except (psycopg2.DatabaseError) as error :
        print ("Error while accessing PostgreSQL table.", error)
    except Exception:
        print ("Error not purtaining to table access.", error)
    finally:
    #closing database connection.
        if(connection):
            connection.close()
            print("PostgreSQL connection is closed")

if __name__=='__main__':
    run()